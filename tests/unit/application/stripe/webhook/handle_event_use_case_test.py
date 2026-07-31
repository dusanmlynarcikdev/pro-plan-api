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


async def test_customer_subscription_created_customer_does_not_exist() -> None:
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
        "customer.subscription.created: "
        "Customer not found: 019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04",
    )


@pytest.mark.parametrize("metadata", ({"customer_id": "not-uuid"}, {}))
async def test_customer_subscription_created_invalid_customer_id(
    metadata: dict,
) -> None:
    use_case = HandleEventUseCase(Mock(CustomerRepository))

    with patch.object(handle_event_use_case_module, "logger") as logger:
        await use_case(
            Event(
                type=WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED,
                data={"metadata": metadata},
            )
        )

    logger.error.assert_called_once_with(
        "customer.subscription.created: "
        f"Invalid metadata customer_id: {metadata.get('customer_id')}"
    )
