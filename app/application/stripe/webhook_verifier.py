from typing import Protocol

from app.application.stripe.webhook_event import WebhookEvent


class WebhookVerifier(Protocol):
    def verify(self, payload: bytes, signature: str) -> WebhookEvent:
        """
        :raises WebhookSignatureError:
        """
        ...
