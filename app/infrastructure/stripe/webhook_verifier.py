from stripe import SignatureVerificationError, Webhook

from app.application.stripe.errors import WebhookVerificationError
from app.application.stripe.webhook_event import WebhookEvent


class WebhookVerifier:
    def __init__(self, secret: str) -> None:
        self._secret = secret

    def verify(self, payload: bytes, signature: str) -> WebhookEvent:
        """
        :raises WebhookVerificationError:
        """
        try:
            event = Webhook.construct_event(payload, signature, self._secret)
        except (ValueError, SignatureVerificationError) as e:
            raise WebhookVerificationError from e

        return WebhookEvent(type=event.type, data=event.data.object.to_dict())
