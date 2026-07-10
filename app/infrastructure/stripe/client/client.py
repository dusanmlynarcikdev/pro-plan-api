from uuid import UUID

from stripe import StripeClient
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.stripe.client.errors import MissingCheckoutSessionUrlError


class Client:
    def __init__(self, api_key: str) -> None:
        self._client = StripeClient(api_key)

    async def create_checkout_session(
        self, price_id: str, subscription_id: UUID
    ) -> str:
        params = self._create_request_params(price_id, subscription_id)

        # todo handle errors
        session = await self._client.v1.checkout.sessions.create_async(params)

        return self._parse_url(session)

    @staticmethod
    def _create_request_params(
        price_id: str, subscription_id: UUID
    ) -> SessionCreateParams:
        return SessionCreateParams(
            client_reference_id=str(subscription_id),
            line_items=[SessionCreateParamsLineItem(price=price_id, quantity=1)],
        )

    @staticmethod
    def _parse_url(session: Session) -> str:
        url = session.url

        if url is None:
            raise MissingCheckoutSessionUrlError

        return url
