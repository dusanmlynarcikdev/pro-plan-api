from unittest.mock import Mock

import pytest
from stripe import StripeClient

from app.infrastructure.stripe.checkout.billing_period import BillingPeriod
from app.infrastructure.stripe.checkout.checkout_client import CheckoutClient


@pytest.mark.parametrize(
    ("billing_period", "price_id"),
    [
        (BillingPeriod.MONTHLY, "price_id_monthly"),
        (BillingPeriod.YEARLY, "price_id_yearly"),
    ],
)
def test_resolve_price_id(billing_period: BillingPeriod, price_id: str) -> None:
    checkout_client = CheckoutClient(
        Mock(StripeClient),
        "price_id_monthly",
        "price_id_yearly",
        "https://example.com/success",
    )

    assert checkout_client._resolve_price_id(billing_period) == price_id
