import logging
from uuid import UUID

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.domain.subscription.errors import SubscriptionNotFoundError
from app.domain.subscription.repository import SubscriptionRepository

logger = logging.getLogger(__name__)


class HandleEventUseCase:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self._repository = repository

    async def __call__(self, event: Event) -> None:
        match event.type:
            case WebhookEventType.CHECKOUT_SESSION_COMPLETED:
                await self._handle_checkout_session_completed(event)

    async def _handle_checkout_session_completed(self, event: Event) -> None:
        client_reference_id = event.data.get("client_reference_id")

        try:
            subscription = await self._repository.get(UUID(client_reference_id))
        except SubscriptionNotFoundError:
            logger.error(
                "Checkout session completed: "
                "Subscription not found for client_reference_id: %s",
                client_reference_id,
            )
            return
        except TypeError, ValueError:
            logger.error(
                "Checkout session completed: Invalid client_reference_id: %s",
                client_reference_id,
            )
            return

        subscription.stripe_customer_id = event.data.get("customer")
        subscription.activate()

        await self._repository.update(subscription)
        await self._repository.commit()
