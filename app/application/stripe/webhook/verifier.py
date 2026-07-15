from typing import Protocol

from app.application.stripe.webhook.event import Event


class Verifier(Protocol):
    def verify(self, payload: bytes, signature: str) -> Event:
        """
        :raises WebhookVerificationError:
        """
        ...
