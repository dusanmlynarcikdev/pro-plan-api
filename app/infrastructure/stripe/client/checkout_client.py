import logging
from uuid import UUID

from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.stripe.client.errors import ClientError

logger = logging.getLogger(__name__)


class CheckoutClient:
    def __init__(self, api_key: str, success_url: str) -> None:
        self._client = StripeClient(api_key)
        self._success_url = success_url

    async def create_session(self, price_id: str, subscription_id: UUID) -> str:
        params = self._create_request_params(price_id, subscription_id)

        try:
            session = await self._client.v1.checkout.sessions.create_async(params)
        except StripeError as e:
            message = e.user_message or str(e)
            logger.error(message)
            raise ClientError(message)

        return self._validate_url(session)

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
    def _validate_url(session: Session) -> str:
        url = session.url

        if url is None:
            message = "Stripe checkout session url is missing"
            logger.error(message)
            raise ClientError(message)

        return url
