from unittest.mock import AsyncMock, Mock

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from stripe import StripeError
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
    SessionCreateParamsSubscriptionData,
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
            "customerExternalId": "user-1",
            "stripePriceId": "price-1",
            "successUrl": "https://example.com/success",
        },
    )
    session.expunge_all()

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": CHECKOUT_URL}

    customer = (await session.exec(select(CustomerSchema))).one()
    assert customer.external_id == "user-1"

    stripe_client.assert_called_once_with("example-api-key")
    stripe_client.return_value.v1.checkout.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(
            customer="customer-1",
            line_items=[SessionCreateParamsLineItem(price="price-1", quantity=1)],
            mode="subscription",
            subscription_data=SessionCreateParamsSubscriptionData(
                metadata={
                    "customer_id": str(customer.id),
                }
            ),
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
            "customerExternalId": "user-1",
            "stripePriceId": "price-1",
            "successUrl": "https://example.com/success",
        },
    )

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.content == b'{"detail":"Unable to create checkout session"}'


def test_invalid_success_url(client: TestClient) -> None:
    response = client.post(
        PATH,
        json={
            "customerExternalId": "user-1",
            "stripePriceId": "price-1",
            "successUrl": "invalid-url",
        },
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert b"successUrl" in response.content
