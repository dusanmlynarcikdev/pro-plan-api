from unittest.mock import Mock

import pytest

from app.application.stripe.billing_period import BillingPeriod
from app.application.stripe.checkout_client import CheckoutClient
from app.application.stripe.create_checkout_session_use_case import (
    CreateCheckoutSessionUseCase,
)
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)


@pytest.mark.parametrize(
    ("billing_period", "expected_price_id"),
    [
        (BillingPeriod.MONTHLY, "price-id-monthly"),
        (BillingPeriod.YEARLY, "price-id-yearly"),
    ],
)
def test_resolve_price_id(
    billing_period: BillingPeriod, expected_price_id: str
) -> None:
    use_case = CreateCheckoutSessionUseCase(
        Mock(GetOrCreateSubscriptionUseCase),
        Mock(CheckoutClient),
        "price-id-monthly",
        "price-id-yearly",
    )

    assert use_case._resolve_price_id(billing_period) == expected_price_id
