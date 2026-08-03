from typing import Protocol

from app.application.stripe.webhook.dtos import Event


class Verifier(Protocol):
    def verify(self, payload: bytes, signature: str) -> Event:
        """
        :raises WebhookVerificationError:
        """
        ...
