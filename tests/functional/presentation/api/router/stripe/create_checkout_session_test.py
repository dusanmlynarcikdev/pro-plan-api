from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch

from fastapi import status
from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from stripe import StripeError
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate

PATH = "/api/stripe/checkout-sessions"
SESSION_URL = "https://checkout.stripe.com/c/pay/cs_test_123"


@fixture
def stripe_client() -> Generator[Mock]:
    with patch(
        "app.infrastructure.stripe.client.checkout_client.StripeClient"
    ) as client:
        client.return_value.v1.checkout.sessions.create_async = AsyncMock(
            return_value=Mock(url=SESSION_URL)
        )
        yield client


async def test_create(
    client: TestClient, session: AsyncSession, stripe_client: Mock
) -> None:
    response = client.post(
        PATH, json={"email": "john@doe.com", "billing_period": "monthly"}
    )
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": SESSION_URL}

    subscription = (await session.exec(select(SubscriptionSchema))).one()
    assert subscription.email == "john@doe.com"
    assert not subscription.is_active

    stripe_client.assert_called_once_with("test")
    stripe_client.return_value.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            client_reference_id=str(subscription.id),
            line_items=[SessionCreateParamsLineItem(price="price-1", quantity=1)],
            mode="subscription",
            success_url="https://example.com/success",
        )
    )


async def test_create_with_existing_subscription_for_yearly_billing_period(
    client: TestClient, session: AsyncSession, stripe_client: Mock
) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    response = client.post(
        PATH, json={"email": "john@doe.com", "billing_period": "yearly"}
    )
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK

    assert len((await session.exec(select(SubscriptionSchema))).all()) == 1

    stripe_client.return_value.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            client_reference_id="019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04",
            line_items=[SessionCreateParamsLineItem(price="price-2", quantity=1)],
            mode="subscription",
            success_url="https://example.com/success",
        )
    )


async def test_stripe_error(
    client: TestClient,
    # Rollback subscription created by request
    session: AsyncSession,
    stripe_client: Mock,
) -> None:
    stripe_client.return_value.v1.checkout.sessions.create_async.side_effect = (
        StripeError("Something went wrong")
    )

    response = client.post(
        PATH, json={"email": "john@doe.com", "billing_period": "monthly"}
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.content == b'{"detail":"Unable to create Stripe checkout session"}'
