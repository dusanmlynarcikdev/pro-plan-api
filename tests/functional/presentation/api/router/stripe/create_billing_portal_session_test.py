from unittest.mock import AsyncMock, Mock

from fastapi import status
from fastapi.testclient import TestClient
from stripe import StripeError
from stripe.params.billing_portal import SessionCreateParams

BILLING_PORTAL_URL = "https://billing.stripe.com/p/session/bps_test_123"
PATH = "/api/stripe/billing-portal/sessions"


async def test_create(client: TestClient, stripe_client: Mock) -> None:
    stripe_client.return_value.v1.billing_portal.sessions.create_async = AsyncMock(
        return_value=Mock(url=BILLING_PORTAL_URL)
    )

    response = client.post(PATH, json={"stripe_customer_id": "customer-1"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"url": BILLING_PORTAL_URL}

    stripe_client.assert_called_once_with("example-api-key")
    stripe_client.return_value.v1.billing_portal.sessions.create_async.assert_awaited_once_with(
        SessionCreateParams(customer="customer-1")
    )


async def test_stripe_error(client: TestClient, stripe_client: Mock) -> None:
    stripe_client.return_value.v1.billing_portal.sessions.create_async.side_effect = (
        StripeError("Something went wrong")
    )

    response = client.post(PATH, json={"stripe_customer_id": "customer-1"})

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert response.content == b'{"detail":"Unable to create billing portal session"}'


def test_invalid_request(client: TestClient) -> None:
    response = client.post(PATH, json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert b"stripe_customer_id" in response.content
