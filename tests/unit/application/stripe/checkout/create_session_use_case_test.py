from unittest.mock import AsyncMock, Mock

from pytest import raises

from app.application.customer.get_or_create_customer_use_case import (
    GetOrCreateCustomerUseCase,
)
from app.application.stripe.checkout.client import Client
from app.application.stripe.checkout.create_session_use_case import CreateSessionUseCase
from app.application.stripe.errors import CustomerAlreadyHasStripeSubscriptionError
from tests.generator.customer import generate_with_subscription


async def test_customer_already_has_subscription() -> None:
    use_case = CreateSessionUseCase(
        AsyncMock(
            GetOrCreateCustomerUseCase,
            return_value=generate_with_subscription(),
        ),
        Mock(Client),
    )

    with raises(CustomerAlreadyHasStripeSubscriptionError):
        await use_case(
            "user-1",
            "price-1",
            "https://example.com/success",
        )
