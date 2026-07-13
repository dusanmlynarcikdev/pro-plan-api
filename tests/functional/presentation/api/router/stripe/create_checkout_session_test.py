from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest
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
from app.presentation.api.dependencies import get_stripe_client
from tests.generator.subscription import generate

PATH = "/api/stripe/checkout/sessions"
SESSION_URL = "https://checkout.stripe.com/c/pay/cs_test_123"


async def test_create_with_existing_subscription(
    client: TestClient, session: AsyncSession, stripe_client: Mock
) -> None:
    session.add(
        SubscriptionSchema.from_domain(generate(stripe_customer_id="customer-1"))
    )
    await session.flush()
    session.expunge_all()

    response = client.post(
        PATH, json={"email": "john@doe.com", "billing_period": "monthly"}
    )
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": SESSION_URL}

    subscription = (await session.exec(select(SubscriptionSchema))).one()
    assert subscription.email == "john@doe.com"
    assert not subscription.is_active

    stripe_client.assert_called_once_with("example-api-key")
    stripe_client.return_value.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            client_reference_id=str(subscription.id),
            customer="customer-1",
            line_items=[SessionCreateParamsLineItem(price="example-id-1", quantity=1)],
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


@pytest.mark.parametrize(
    "request_body, expected_content",
    (
        (
            {
                "email": "john",
                "billing_period": "monthly",
            },
            b"email",
        ),
        (
            {
                "email": "john@doe.com",
                "billing_period": "weekly",
            },
            b"billing_period",
        ),
    ),
)
def test_invalid_request(
    client: TestClient, request_body: dict[str, str], expected_content: bytes
) -> None:
    response = client.post(PATH, json=request_body)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert expected_content in response.content


@fixture
def stripe_client() -> Generator[Mock]:
    with patch("app.presentation.api.dependencies.StripeClient") as client:
        client.return_value.v1.checkout.sessions.create_async = AsyncMock(
            return_value=Mock(url=SESSION_URL)
        )
        yield client

    get_stripe_client.cache_clear()
