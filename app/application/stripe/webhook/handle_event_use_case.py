import logging
from uuid import UUID

from app.application.email.message import Message
from app.application.email.sender import Sender
from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.domain.subscription.errors import SubscriptionNotFoundError
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.subscription import Subscription

logger = logging.getLogger(__name__)


class HandleEventUseCase:
    def __init__(
        self, email_sender: Sender, repository: SubscriptionRepository
    ) -> None:
        self._email_sender = email_sender
        self._repository = repository

    async def __call__(self, event: Event) -> None:
        match event.type:
            case WebhookEventType.CHECKOUT_SESSION_COMPLETED:
                await self._handle_checkout_session_completed(event)

    async def _get_subscription(
        self, client_reference_id: str | None
    ) -> Subscription | None:
        try:
            subscription_id = UUID(client_reference_id)
        except TypeError, ValueError:
            logger.error(
                "Checkout session completed: Invalid client_reference_id: %s",
                client_reference_id,
            )
            return None

        try:
            return await self._repository.get(subscription_id)
        except SubscriptionNotFoundError:
            logger.error(
                "Checkout session completed: Subscription not found for id: %s",
                subscription_id,
            )
            return None

    async def _handle_checkout_session_completed(self, event: Event) -> None:
        subscription = await self._get_subscription(
            event.data.get("client_reference_id")
        )

        if subscription is None:
            return

        subscription.stripe_customer_id = event.data.get("customer")
        subscription.activate()

        await self._repository.update(subscription)
        await self._repository.commit()

        await self._email_sender.send(
            Message(
                subscription.email,
                "Pro plan activated",
                "Congratulations! Your Pro plan has been successfully activated.",
            )
        )
