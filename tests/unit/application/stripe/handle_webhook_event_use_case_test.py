from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.application.stripe import (
    handle_webhook_event_use_case as handle_webhook_event_use_case_module,
)
from app.application.stripe.enums import WebhookEventType
from app.application.stripe.handle_webhook_event_use_case import (
    HandleWebhookEventUseCase,
)
from app.application.stripe.webhook_event import WebhookEvent
from app.domain.subscription.errors import SubscriptionNotFoundError
from app.domain.subscription.repository import SubscriptionRepository


@pytest.mark.parametrize(
    "client_reference_id",
    (None, "not-a-uuid"),
)
async def test_checkout_session_completed_invalid_client_reference_id(
    client_reference_id: str | None,
) -> None:
    use_case = HandleWebhookEventUseCase(Mock(SubscriptionRepository))

    with patch.object(handle_webhook_event_use_case_module, "logger") as logger:
        await use_case(
            WebhookEvent(
                type=WebhookEventType.CHECKOUT_SESSION_COMPLETED,
                data={"client_reference_id": client_reference_id},
            )
        )

    logger.error.assert_called_once_with(
        "Checkout session completed: Invalid client_reference_id: %s",
        client_reference_id,
    )


async def test_checkout_session_completed_subscription_not_found() -> None:
    repository = Mock(SubscriptionRepository)
    repository.get = AsyncMock(side_effect=SubscriptionNotFoundError)

    use_case = HandleWebhookEventUseCase(repository)

    with patch.object(handle_webhook_event_use_case_module, "logger") as logger:
        await use_case(
            WebhookEvent(
                type=WebhookEventType.CHECKOUT_SESSION_COMPLETED,
                data={"client_reference_id": "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"},
            )
        )

    logger.error.assert_called_once_with(
        "Checkout session completed: "
        "Subscription not found for client_reference_id: %s",
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04",
    )
