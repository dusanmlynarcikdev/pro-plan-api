import logging
from uuid import UUID

from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
)

from app.infrastructure.stripe.checkout.billing_period import BillingPeriod
from app.infrastructure.stripe.checkout.checkout_error import CheckoutError

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
        self, billing_period: BillingPeriod, subscription_id: UUID
    ) -> str:
        price_id = self._resolve_price_id(billing_period)
        request_params = self._create_request_params(price_id, subscription_id)

        try:
            session = await self._client.v1.checkout.sessions.create_async(
                request_params
            )
        except StripeError as e:
            logger.error(e.user_message)
            raise CheckoutError(e.user_message)

        return self._validate_response_url(session)

    def _create_request_params(
        self, price_id: str, subscription_id: UUID
    ) -> SessionCreateParams:
        return SessionCreateParams(
            client_reference_id=str(subscription_id),
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
            message = "Stripe checkout session url is missing"
            logger.error(message)
            raise CheckoutError(message)

        return url
