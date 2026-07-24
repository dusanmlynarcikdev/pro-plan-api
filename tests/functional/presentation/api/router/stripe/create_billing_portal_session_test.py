from unittest.mock import AsyncMock, Mock

from fastapi import status
from fastapi.testclient import TestClient
from stripe import StripeError
from stripe.params.billing_portal import SessionCreateParams

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate

BILLING_PORTAL_URL = "https://billing.stripe.com/p/session/bps_test_123"
PATH = "/api/customers/{external_id}/stripe/billing-portal/sessions"


async def test_create(
    client: TestClient, session: AsyncMock, stripe_client: Mock
) -> None:
    customer = generate()
    customer._stripe_id = "customer-1"
    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    stripe_client.return_value.v1.billing_portal.sessions.create_async = AsyncMock(
        return_value=Mock(url=BILLING_PORTAL_URL)
    )

    response = client.post(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": BILLING_PORTAL_URL}

    stripe_client.assert_called_once_with("example-api-key")
    stripe_client.return_value.v1.billing_portal.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(customer="customer-1")
    )


async def test_stripe_error(
    client: TestClient, session: AsyncMock, stripe_client: Mock
) -> None:
    customer = generate()
    customer._stripe_id = "customer-1"
    session.add(CustomerSchema.from_domain(customer))
    await session.flush()
    session.expunge_all()

    stripe_client.return_value.v1.billing_portal.sessions.create_async.side_effect = (
        StripeError("Something went wrong")
    )

    response = client.post(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_502_BAD_GATEWAY
    assert response.content == b'{"detail":"Unable to create billing portal session"}'


async def test_customer_does_not_exist(client: TestClient) -> None:
    response = client.post(PATH.format(external_id="user-1"))

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.content == b'{"detail":"Customer not found"}'
