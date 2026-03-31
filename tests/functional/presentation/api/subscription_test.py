from decimal import Decimal

from fastapi import status
from pytest import mark
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.domain.subscription.period import Period
from app.domain.subscription.state import State
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate


async def test_create(client: TestClient, session: AsyncSession) -> None:
    response = client.post(
        "/subscriptions",
        json={
            "email": "john@doe.com",
            "price": {"amount": 123.45, "currency": "USD"},
            "period": "monthly",
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    repository_subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert repository_subscription.email == "john@doe.com"
    assert repository_subscription.amount == Decimal("123.45")
    assert repository_subscription.currency == "USD"
    assert repository_subscription.period == Period.MONTHLY
    assert repository_subscription.next_payment_date is None
    assert repository_subscription.state == State.NEW


async def test_update(client: TestClient, session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.post(
        "/subscriptions",
        json={
            "email": "john@doe.com",
            "price": {"amount": 124.55, "currency": "EUR"},
            "period": "yearly",
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.content == b""

    repository_subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert repository_subscription.email == "john@doe.com"
    assert repository_subscription.amount == Decimal("124.55")
    assert repository_subscription.currency == "EUR"
    assert repository_subscription.period == Period.YEARLY
    assert repository_subscription.next_payment_date is None
    assert repository_subscription.state == State.NEW


@mark.parametrize(
    "json, expected_status, expected_content",
    [
        (
            {
                "email": "doe.com",
                "price": {"amount": 124.55, "currency": "EUR"},
                "period": "yearly",
            },
            status.HTTP_400_BAD_REQUEST,
            b'{"message":"Invalid email"}',
        ),
        (
            {
                "email": "john@doe.com",
                "price": {"amount": -1, "currency": "EUR"},
                "period": "yearly",
            },
            status.HTTP_400_BAD_REQUEST,
            b'{"message":"Amount must be greater than 0"}',
        ),
        (
            {
                "email": "john@doe.com",
                "price": {"amount": 124.55, "currency": "XYZ"},
                "period": "yearly",
            },
            status.HTTP_400_BAD_REQUEST,
            b'{"message":"Invalid currency"}',
        ),
        (
            {
                "email": "john@doe.com",
                "price": {"amount": 124.55, "currency": "EUR"},
                "period": "unknown",
            },
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            b'"loc":["body","period"]',
        ),
    ],
)
async def test_invalid_value(
    client: TestClient,
    json: dict[str, str | dict[str, str | float]],
    expected_status: int,
    expected_content: bytes,
) -> None:
    response = client.post("/subscriptions", json=json)

    assert response.status_code == expected_status
    assert expected_content in response.content
