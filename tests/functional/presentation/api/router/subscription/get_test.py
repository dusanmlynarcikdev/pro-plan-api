from datetime import date
from unittest.mock import patch

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate

PATH = "/api/subscriptions/{email}"


async def test_get_subscription(client: TestClient, session: AsyncSession) -> None:
    subscription = generate()
    subscription.renew(date(2026, 1, 1))
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()
    session.expunge_all()

    with patch("app.presentation.api.router.subscription.get.date") as mock_date:
        mock_date.today.return_value = date(2026, 1, 1)
        response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "email": "john@doe.com",
        "period": "monthly",
        "expires_at": "2026-02-01",
        "is_active": True,
    }


async def test_get_subscription_another_subscription_exists(
    client: TestClient, session: AsyncSession
) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.get(PATH.format(email="john2@doe.com"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Subscription not found"}'


async def test_get_subscription_subscription_does_not_exist(client: TestClient) -> None:
    response = client.get(PATH.format(email="john@doe.com"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Subscription not found"}'


def test_get_subscription_invalid_email(client: TestClient) -> None:
    response = client.get(PATH.format(email="johndoe.com"))

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.content == b'{"detail":"Invalid email"}'
