from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.persistence.schema.customer import CustomerSchema
from tests.generator.customer import generate

PATH = "/api/customers/{external_id}"


async def test_get(client: TestClient, session: AsyncSession) -> None:
    customer = generate()
    customer.link_stripe_subscription("customer-1")

    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    response = client.get(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'{"canAccessStripeBillingPortal":true,"hasPro":true}'


async def test_get_customer_does_not_exist(client: TestClient) -> None:
    response = client.get(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Customer not found"}'
