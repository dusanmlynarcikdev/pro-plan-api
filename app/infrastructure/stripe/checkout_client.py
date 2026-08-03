from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsLineItem,
    SessionCreateParamsSubscriptionData,
)

from app.application.stripe.enums import SubscriptionMetadataKey
from app.application.stripe.errors import UnableToCreateCheckoutSessionError


class CheckoutClient:
    def __init__(
        self,
        client: StripeClient,
    ) -> None:
        self._client = client

    async def create_session(
        self,
        customer_id: str,
        stripe_customer_id: str | None,
        price_id: str,
        success_url: str,
        trial_days: int | None,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        request_params = self._create_request_params(
            stripe_customer_id,
            price_id,
            self._create_subscription_request_params(customer_id, trial_days),
            success_url,
        )

        try:
            session = await self._client.v1.checkout.sessions.create_async(
                request_params
            )
        except StripeError as e:
            raise UnableToCreateCheckoutSessionError from e

        return self._validate_response_url(session)

    @staticmethod
    def _create_request_params(
        stripe_customer_id: str | None,
        price_id: str,
        subscription_data: SessionCreateParamsSubscriptionData,
        success_url: str,
    ) -> SessionCreateParams:
        params = SessionCreateParams(
            line_items=[SessionCreateParamsLineItem(price=price_id, quantity=1)],
            mode="subscription",
            subscription_data=subscription_data,
            success_url=success_url,
        )

        if stripe_customer_id is not None:
            params.update(customer=stripe_customer_id)

        return params

    @staticmethod
    def _create_subscription_request_params(
        customer_id: str,
        trial_days: int | None,
    ) -> SessionCreateParamsSubscriptionData:
        params = SessionCreateParamsSubscriptionData(
            metadata={
                SubscriptionMetadataKey.CUSTOMER_ID: customer_id,
            }
        )

        if trial_days is not None:
            params.update(trial_period_days=trial_days)

        return params

    @staticmethod
    def _validate_response_url(session: Session) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        url = session.url

        if url is None:
            raise UnableToCreateCheckoutSessionError from ValueError(
                "Checkout session url is missing"
            )

        return url
