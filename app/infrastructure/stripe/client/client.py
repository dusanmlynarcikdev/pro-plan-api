import logging
from uuid import UUID

from stripe import StripeClient
from stripe import StripeError as StripeApiError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.stripe.client.errors import StripeError

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, api_key: str, success_url: str) -> None:
        self._client = StripeClient(api_key)
        self._success_url = success_url

    async def create_checkout_session(
        self, price_id: str, subscription_id: UUID
    ) -> str:
        params = self._create_request_params(price_id, subscription_id)

        try:
            session = await self._client.v1.checkout.sessions.create_async(params)
        except StripeApiError as e:
            message = e.user_message or str(e)
            self._log_error(message)
            raise StripeError(message)

        return self._parse_url(session)

    def _create_request_params(
        self, price_id: str, subscription_id: UUID
    ) -> SessionCreateParams:
        return SessionCreateParams(
            client_reference_id=str(subscription_id),
            line_items=[SessionCreateParamsLineItem(price=price_id, quantity=1)],
            mode="subscription",
            success_url=self._success_url,
        )

    @staticmethod
    def _log_error(message: str) -> None:
        logger.error(f"Stripe: {message}")

    @staticmethod
    def _parse_url(session: Session) -> str:
        url = session.url

        if url is None:
            message = f"Stripe checkout session url is missing"
            Client._log_error(message)
            raise StripeError(message)

        return url
