from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.persistence.schema.customer import CustomerSchema
from tests.generator.customer import generate

PATH = "/api/customers/{email}"


async def test_get(client: TestClient, session: AsyncSession) -> None:
    session.add(CustomerSchema.from_domain(generate(stripe_id="customer-1")))
    await session.flush()
    session.expunge_all()

    response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'{"has_pro":false,"stripe_id":"customer-1"}'


async def test_get_customer_does_not_exist(client: TestClient) -> None:
    response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Customer not found"}'


def test_get_invalid_email(client: TestClient) -> None:
    response = client.get(PATH.format(email="johndoe.com"))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.content == b'{"detail":"Invalid email"}'
