from app.application.customer.get_or_create_customer_use_case import (
    GetOrCreateCustomerUseCase,
)
from app.application.stripe.checkout.client import Client
from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.application.stripe.errors import CustomerAlreadyHasStripeSubscriptionError


class CreateSessionUseCase:
    def __init__(
        self,
        get_or_create_customer: GetOrCreateCustomerUseCase,
        client: Client,
    ) -> None:
        self._get_or_create_customer = get_or_create_customer
        self._client = client

    async def __call__(
        self,
        customer_external_id: str,
        billing_period: CheckoutSessionBillingPeriod,
        success_url: str,
    ) -> str:
        """
        :raises CustomerAlreadyHasStripeSubscriptionError:
        :raises UnableToCreateCheckoutSessionError:
        """
        customer = await self._get_or_create_customer(customer_external_id)

        if customer.has_stripe_subscription():
            raise CustomerAlreadyHasStripeSubscriptionError

        return await self._client.create_session(
            billing_period, str(customer.id), customer.stripe_id, success_url
        )
