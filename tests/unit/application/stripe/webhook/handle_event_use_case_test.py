from unittest.mock import AsyncMock, Mock, patch
from uuid import UUID

import pytest

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook import (
    handle_event_use_case as handle_event_use_case_module,
)
from app.application.stripe.webhook.event import Event
from app.application.stripe.webhook.handle_event_use_case import HandleEventUseCase
from app.domain.customer.errors import CustomerNotFoundError
from app.domain.customer.repository import CustomerRepository


async def test_customer_subscription_deleted_customer_does_not_exist() -> None:
    repository = Mock(CustomerRepository)
    repository.find_one_by_stripe_id = AsyncMock(return_value=None)

    use_case = HandleEventUseCase(repository)

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED,
                data={"customer": "cus_123"},
            )
        )

    logger.error.assert_called_once_with(
        "Customer subscription deleted: Customer not found for id: %s",
        "cus_123",
    )


@pytest.mark.parametrize(
    "client_reference_id",
    (None, "not-a-uuid"),
)
async def test_checkout_session_completed_invalid_client_reference_id(
    client_reference_id: str | None,
) -> None:
    use_case = HandleEventUseCase(Mock(CustomerRepository))

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CHECKOUT_SESSION_COMPLETED,
                data={"client_reference_id": client_reference_id},
            )
        )

    logger.error.assert_called_once_with(
        "Checkout session completed: Invalid client_reference_id: %s",
        client_reference_id,
    )


async def test_checkout_session_completed_customer_not_found() -> None:
    repository = Mock(CustomerRepository)
    repository.get = AsyncMock(side_effect=CustomerNotFoundError)

    use_case = HandleEventUseCase(repository)

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CHECKOUT_SESSION_COMPLETED,
                data={"client_reference_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"},
            )
        )

    logger.error.assert_called_once_with(
        "Checkout session completed: Customer not found for id: %s",
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    )
