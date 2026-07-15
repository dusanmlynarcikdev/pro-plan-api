from app.application.stripe.checkout_client import CheckoutClient
from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)
from app.domain.subscription.email import Email


class CreateCheckoutSessionUseCase:
    def __init__(
        self,
        get_or_create_subscription: GetOrCreateSubscriptionUseCase,
        checkout_client: CheckoutClient,
    ) -> None:
        self._get_or_create_subscription = get_or_create_subscription
        self._checkout_client = checkout_client

    async def __call__(
        self, email: Email, billing_period: CheckoutSessionBillingPeriod
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        subscription = await self._get_or_create_subscription(email)

        return await self._checkout_client.create_session(
            billing_period, str(subscription.id), subscription.stripe_customer_id
        )
