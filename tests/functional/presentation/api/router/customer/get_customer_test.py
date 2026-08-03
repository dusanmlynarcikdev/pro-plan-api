from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate_with_stripe

PATH = "/api/customers/{external_id}"


async def test_get(client: TestClient, session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate_with_stripe()))
    await session.flush()
    session.expunge_all()

    response = client.get(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_200_OK
    assert response.content == (
        b'{"stripe":{"canAccessBillingPortal":true,"subscription":'
        b'{"cancelAt":"2027-02-02T13:35:50Z","isActive":true,"isTrial":true,'
        b'"periodEndAt":"2026-01-01T12:30:45Z","productId":"product-1"}}}'
    )


async def test_get_customer_does_not_exist(client: TestClient) -> None:
    response = client.get(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Customer not found"}'
