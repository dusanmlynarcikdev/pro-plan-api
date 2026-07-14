from app.application.stripe.webhook_event import WebhookEvent


class HandleWebhookEventUseCase:
    async def __call__(self, event: WebhookEvent) -> None: ...
