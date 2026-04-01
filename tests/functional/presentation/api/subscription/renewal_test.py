from datetime import date
from decimal import Decimal
from unittest.mock import patch
from uuid import UUID

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.infrastructure.persistence.schema.payment import PaymentSchema
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate


async def test_success(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with patch("app.application.subscription.renewal_command.date") as mock_date:
        mock_date.today.return_value = date(2026, 1, 1)
        response = client.post("/subscriptions/john@doe.com/renewal")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.content == b""

    repository_subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert repository_subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_subscription.email == "john@doe.com"
    assert repository_subscription.amount == Decimal("1")
    assert repository_subscription.currency == "USD"
    assert repository_subscription.period == "monthly"
    assert repository_subscription.next_payment_date == date(2026, 2, 1)
    assert repository_subscription.state == "active"

    repository_payment = (await session.exec(select(PaymentSchema))).one()

    assert repository_payment.subscription_id == UUID(
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"
    )
    assert repository_payment.amount == Decimal("1")
    assert repository_payment.currency == "USD"
    assert repository_payment.paid_at == date(2026, 1, 1)


async def test_unknown_email(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.post("/subscriptions/john2@doe.com/renewal")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"message":"Subscription not found"}'


def test_invalid_email(client: TestClient) -> None:
    response = client.post("/subscriptions/johndoe.com/renewal")

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.content == b'{"message":"Invalid email"}'
