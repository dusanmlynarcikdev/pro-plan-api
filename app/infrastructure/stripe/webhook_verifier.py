from stripe import SignatureVerificationError, Webhook

from app.application.stripe.errors import WebhookVerificationError
from app.application.stripe.webhook.event import Event


class WebhookVerifier:
    def __init__(self, secret: str) -> None:
        self._secret = secret

    def verify(self, payload: bytes, signature: str) -> Event:
        """
        :raises WebhookVerificationError:
        """
        try:
            event = Webhook.construct_event(payload, signature, self._secret)
        except SignatureVerificationError as e:
            raise WebhookVerificationError from e

        return Event(type=event.type, data=event.data.object.to_dict())
