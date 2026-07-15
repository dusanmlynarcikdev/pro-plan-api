import logging

from app.application.stripe.errors import WebhookVerificationError
from app.application.stripe.webhook.event import Event
from app.application.stripe.webhook.verifier import Verifier

logger = logging.getLogger(__name__)


class VerifyUseCase:
    def __init__(self, verifier: Verifier) -> None:
        self._verifier = verifier

    async def __call__(self, payload: bytes, signature: str) -> Event:
        """
        :raises WebhookVerificationError:
        """
        try:
            return self._verifier.verify(payload, signature)
        except WebhookVerificationError as e:
            logger.error("Webhook verification failed: %s", e.__cause__)
            raise
