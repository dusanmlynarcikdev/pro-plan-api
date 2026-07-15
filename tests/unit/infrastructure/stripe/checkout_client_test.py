from unittest.mock import Mock

import pytest
from stripe import StripeClient

from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.infrastructure.stripe.checkout_client import CheckoutClient


@pytest.mark.parametrize(
    ("billing_period", "expected_price_id"),
    (
        (CheckoutSessionBillingPeriod.MONTHLY, "price-id-monthly"),
        (CheckoutSessionBillingPeriod.YEARLY, "price-id-yearly"),
    ),
)
def test_resolve_price_id(
    billing_period: CheckoutSessionBillingPeriod, expected_price_id: str
) -> None:
    checkout_client = CheckoutClient(
        Mock(StripeClient),
        "price-id-monthly",
        "price-id-yearly",
        "https://example.com/success",
    )

    assert checkout_client._resolve_price_id(billing_period) == expected_price_id
