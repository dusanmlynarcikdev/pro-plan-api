from unittest.mock import AsyncMock, Mock

from pytest import raises

from app.application.stripe.checkout.client import Client
from app.application.stripe.checkout.create_session_use_case import CreateSessionUseCase
from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.application.stripe.errors import SubscriptionActiveInStripeError
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)
from app.domain.subscription.email import Email
from tests.generator.subscription import generate


async def test_subscription_active_in_stripe() -> None:
    subscription = generate(stripe_customer_id="cus_123")
    subscription.activate()

    use_case = CreateSessionUseCase(
        AsyncMock(
            GetOrCreateSubscriptionUseCase,
            return_value=subscription,
        ),
        Mock(Client),
    )

    with raises(SubscriptionActiveInStripeError):
        await use_case(Email("john@doe.com"), CheckoutSessionBillingPeriod.MONTHLY)
