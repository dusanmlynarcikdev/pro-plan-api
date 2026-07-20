from unittest.mock import AsyncMock, Mock

from pytest import raises

from app.application.stripe.billing_portal.client import Client
from app.application.stripe.billing_portal.create_session_use_case import (
    CreateSessionUseCase,
)
from app.application.stripe.errors import CustomerIsNotLinkedToStripeError
from app.domain.customer.repository import CustomerRepository
from tests.generator.customer import generate


async def test_customer_is_not_linked_to_stripe() -> None:
    customer_repository = AsyncMock(CustomerRepository)
    customer_repository.get_by_external_id.return_value = generate()

    use_case = CreateSessionUseCase(Mock(Client), customer_repository)

    with raises(CustomerIsNotLinkedToStripeError):
        await use_case("user-1")
