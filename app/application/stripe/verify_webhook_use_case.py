import logging

from app.application.stripe.errors import WebhookVerificationError
from app.application.stripe.webhook_event import WebhookEvent
from app.application.stripe.webhook_verifier import WebhookVerifier

logger = logging.getLogger(__name__)


class VerifyWebhookUseCase:
    def __init__(self, verifier: WebhookVerifier) -> None:
        self._verifier = verifier

    async def __call__(self, payload: bytes, signature: str) -> WebhookEvent:
        """
        :raises WebhookVerificationError:
        """
        try:
            return self._verifier.verify(payload, signature)
        except WebhookVerificationError as e:
            logger.error("Webhook verification failed: %s", e.__cause__)
            raise
