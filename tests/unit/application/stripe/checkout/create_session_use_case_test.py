from unittest.mock import AsyncMock, Mock

from pytest import raises

from app.application.customer.get_or_create_customer_use_case import (
    GetOrCreateCustomerUseCase,
)
from app.application.stripe.checkout.client import Client
from app.application.stripe.checkout.create_session_use_case import CreateSessionUseCase
from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.application.stripe.errors import CustomerAlreadyHasStripeSubscriptionError
from tests.generator.customer import generate


async def test_subscription_active_in_stripe() -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")

    use_case = CreateSessionUseCase(
        AsyncMock(
            GetOrCreateCustomerUseCase,
            return_value=customer,
        ),
        Mock(Client),
    )

    with raises(CustomerAlreadyHasStripeSubscriptionError):
        await use_case(
            "user-1",
            CheckoutSessionBillingPeriod.MONTHLY,
            "https://example.com/success",
        )
