from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from stripe import StripeError
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate

CHECKOUT_URL = "https://checkout.stripe.com/c/pay/cs_test_123"
PATH = "/api/customers/stripe/checkout/sessions"


async def test_create_with_existing_customer(
    client: TestClient, session: AsyncSession, stripe_client: Mock
) -> None:
    stripe_client.return_value.v1.checkout.sessions.create_async = AsyncMock(
        return_value=Mock(url=CHECKOUT_URL)
    )

    customer = generate()
    customer._stripe_id = "customer-1"
    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    response = client.post(
        PATH,
        json={
            "billingPeriod": "monthly",
            "customerExternalId": "user-1",
            "successUrl": "https://example.com/success",
        },
    )
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": CHECKOUT_URL}

    customer = (await session.exec(select(CustomerSchema))).one()
    assert customer.external_id == "user-1"
    assert not customer.has_pro

    stripe_client.assert_called_once_with("example-api-key")
    stripe_client.return_value.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            client_reference_id=str(customer.id),
            customer="customer-1",
            line_items=[SessionCreateParamsLineItem(price="example-id-1", quantity=1)],
            mode="subscription",
            success_url="https://example.com/success",
        )
    )


async def test_stripe_error(
    client: TestClient,
    # Rollback customer created by request
    session: AsyncSession,
    stripe_client: Mock,
) -> None:
    stripe_client.return_value.v1.checkout.sessions.create_async.side_effect = (
        StripeError("Something went wrong")
    )

    response = client.post(
        PATH,
        json={
            "billingPeriod": "monthly",
            "customerExternalId": "user-1",
            "successUrl": "https://example.com/success",
        },
    )

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.content == b'{"detail":"Unable to create checkout session"}'


@pytest.mark.parametrize(
    ("request_body", "expected_response"),
    (
        (
            {
                "billingPeriod": "weekly",
                "customerExternalId": "user-1",
                "successUrl": "https://example.com/success",
            },
            b"billingPeriod",
        ),
        (
            {
                "billingPeriod": "monthly",
                "customerExternalId": "user-1",
                "successUrl": "invalid-url",
            },
            b"successUrl",
        ),
    ),
)
def test_invalid_request(
    client: TestClient, request_body: dict[str, str], expected_response: bytes
) -> None:
    response = client.post(
        PATH,
        json=request_body,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert expected_response in response.content
