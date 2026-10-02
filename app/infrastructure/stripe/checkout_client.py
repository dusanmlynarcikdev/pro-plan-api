from stripe import StripeClient, StripeError
from stripe.checkout import Session
from stripe.params.checkout import (
    SessionCreateParams,
    SessionCreateParamsAutomaticTax,
    SessionCreateParamsCustomerUpdate,
    SessionCreateParamsLineItem,
    SessionCreateParamsNameCollection,
    SessionCreateParamsNameCollectionBusiness,
    SessionCreateParamsSubscriptionData,
    SessionCreateParamsTaxIdCollection,
)

from app.application.stripe.enums import SubscriptionMetadataKey
from app.application.stripe.errors import UnableToCreateCheckoutSessionError

_AUTOMATIC_TAX_REQUEST_PARAMS = SessionCreateParams(
    automatic_tax=SessionCreateParamsAutomaticTax(enabled=True),
    billing_address_collection="required",
)
_BUSINESS_CUSTOMERS_REQUEST_PARAMS = SessionCreateParams(
    name_collection=SessionCreateParamsNameCollection(
        business=SessionCreateParamsNameCollectionBusiness(enabled=True, optional=True)
    ),
    tax_id_collection=SessionCreateParamsTaxIdCollection(enabled=True),
)


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
        automatic_tax: bool,
        business_customers: bool,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        request_params = self._create_request_params(
            stripe_customer_id,
            price_id,
            self._create_subscription_request_params(customer_id, trial_days),
            self._create_customer_update_request_params(
                automatic_tax, business_customers
            ),
            success_url,
            automatic_tax,
            business_customers,
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
        customer_update: SessionCreateParamsCustomerUpdate,
        success_url: str,
        automatic_tax: bool,
        business_customers: bool,
    ) -> SessionCreateParams:
        params = SessionCreateParams(
            line_items=[SessionCreateParamsLineItem(price=price_id, quantity=1)],
            mode="subscription",
            subscription_data=subscription_data,
            success_url=success_url,
        )

        if automatic_tax:
            params.update(_AUTOMATIC_TAX_REQUEST_PARAMS)

        if business_customers:
            params.update(_BUSINESS_CUSTOMERS_REQUEST_PARAMS)

        if stripe_customer_id is not None:
            params.update(customer=stripe_customer_id)

            if customer_update:
                params.update(customer_update=customer_update)

        return params

    @staticmethod
    def _create_customer_update_request_params(
        automatic_tax: bool,
        business_customers: bool,
    ) -> SessionCreateParamsCustomerUpdate:
        params = SessionCreateParamsCustomerUpdate()

        if automatic_tax:
            params.update(address="auto")

        if business_customers:
            params.update(name="auto")

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
