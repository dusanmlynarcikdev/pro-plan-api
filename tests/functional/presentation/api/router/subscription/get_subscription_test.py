from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate

PATH = "/api/subscriptions/{email}"


async def test_get(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_200_OK
    assert response.content == b'{"is_active":false}'


async def test_get_subscription_does_not_exist(client: TestClient) -> None:
    response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Subscription not found"}'


def test_get_invalid_email(client: TestClient) -> None:
    response = client.get(PATH.format(email="johndoe.com"))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.content == b'{"detail":"Invalid email"}'
