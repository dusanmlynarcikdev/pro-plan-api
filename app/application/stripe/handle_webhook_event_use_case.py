import logging

from app.application.stripe.webhook_event import WebhookEvent

logger = logging.getLogger(__name__)


class HandleWebhookEventUseCase:
    async def __call__(self, event: WebhookEvent) -> None: ...
