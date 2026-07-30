from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook import (
    handle_event_use_case as handle_event_use_case_module,
)
from app.application.stripe.webhook.event import Event
from app.application.stripe.webhook.handle_event_use_case import HandleEventUseCase
from app.domain.customer.errors import CustomerNotFoundError
from app.domain.customer.repository import CustomerRepository


async def test_customer_subscription_created_customer_not_found() -> None:
    repository = Mock(CustomerRepository)
    repository.get = AsyncMock(side_effect=CustomerNotFoundError)

    use_case = HandleEventUseCase(repository)

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED,
                data={
                    "metadata": {"customer_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"}
                },
            )
        )

    logger.error.assert_called_once_with(
        "Customer subscription created: Customer not found for id: "
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04",
    )


@pytest.mark.parametrize(
    ("metadata", "expected_log"),
    (
        (
            {"customer_id": "not-a-uuid"},
            "Customer subscription created: Invalid metadata customer_id: not-a-uuid",
        ),
        ({}, "Customer subscription created: Invalid metadata customer_id: None"),
    ),
)
async def test_customer_subscription_created_invalid_customer_id(
    metadata: dict, expected_log: str
) -> None:
    use_case = HandleEventUseCase(Mock(CustomerRepository))

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED,
                data={"metadata": metadata},
            )
        )

    logger.error.assert_called_once_with(expected_log)


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
