import logging
from uuid import UUID

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook_event import WebhookEvent
from app.domain.subscription.errors import SubscriptionNotFoundError
from app.domain.subscription.repository import SubscriptionRepository

logger = logging.getLogger(__name__)


class HandleWebhookEventUseCase:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self._repository = repository

    async def __call__(self, event: WebhookEvent) -> None:
        match event.type:
            case WebhookEventType.CHECKOUT_SESSION_COMPLETED:
                await self._handle_checkout_session_completed(event)

    async def _handle_checkout_session_completed(self, event: WebhookEvent) -> None:
        try:
            subscription_id = UUID(event.data.get("client_reference_id"))
        except ValueError as e:
            logger.error("Invalid client_reference_id: %s", e)
            return

        try:
            subscription = await self._repository.get(subscription_id)
        except SubscriptionNotFoundError:
            logger.error(
                "Subscription not found for client_reference_id: %s", subscription_id
            )
            return

        subscription.stripe_customer_id = event.data.get("customer")
        subscription.activate()

        await self._repository.update(subscription)
        await self._repository.commit()
