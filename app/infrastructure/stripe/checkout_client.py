import logging

from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.application.stripe.errors import CheckoutError

logger = logging.getLogger(__name__)


class CheckoutClient:
    def __init__(self, client: StripeClient, success_url: str) -> None:
        self._client = client
        self._success_url = success_url

    async def create_session(self, price_id: str, client_reference_id: str) -> str:
        request_params = self._create_request_params(price_id, client_reference_id)

        try:
            session = await self._client.v1.checkout.sessions.create_async(
                request_params
            )
        except StripeError as e:
            message = e.user_message
            logger.error(message)
            raise CheckoutError(message)

        return self._validate_response_url(session)

    def _create_request_params(
        self, price_id: str, client_reference_id: str
    ) -> SessionCreateParams:
        return SessionCreateParams(
            client_reference_id=client_reference_id,
            line_items=[SessionCreateParamsLineItem(price=price_id, quantity=1)],
            mode="subscription",
            success_url=self._success_url,
        )

    @staticmethod
    def _validate_response_url(session: Session) -> str:
        url = session.url

        if url is None:
            message = "Stripe checkout session url is missing"
            logger.error(message)
            raise CheckoutError(message)

        return url
