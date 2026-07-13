import logging

from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.application.stripe.enums import BillingPeriod
from app.application.stripe.errors import CheckoutError

logger = logging.getLogger(__name__)


class CheckoutClient:
    def __init__(
        self,
        client: StripeClient,
        price_id_monthly: str,
        price_id_yearly: str,
        success_url: str,
    ) -> None:
        self._client = client
        self._price_id_monthly = price_id_monthly
        self._price_id_yearly = price_id_yearly
        self._success_url = success_url

    async def create_session(
        self, billing_period: BillingPeriod, client_reference_id: str
    ) -> str:
        price_id = self._resolve_price_id(billing_period)
        request_params = self._create_request_params(price_id, client_reference_id)

        try:
            session = await self._client.v1.checkout.sessions.create_async(
                request_params
            )
        except StripeError as e:
            logger.error(e.user_message)
            raise CheckoutError()

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

    def _resolve_price_id(self, billing_period: BillingPeriod) -> str:
        match billing_period:
            case BillingPeriod.MONTHLY:
                return self._price_id_monthly
            case BillingPeriod.YEARLY:
                return self._price_id_yearly

    @staticmethod
    def _validate_response_url(session: Session) -> str:
        url = session.url

        if url is None:
            logger.error("Stripe checkout session url is missing")
            raise CheckoutError()

        return url
