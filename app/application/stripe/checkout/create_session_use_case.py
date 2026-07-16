from app.application.stripe.checkout.client import Client
from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.application.stripe.errors import SubscriptionActiveInStripeError
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)
from app.domain.subscription.email import Email


class CreateSessionUseCase:
    def __init__(
        self,
        get_or_create_subscription: GetOrCreateSubscriptionUseCase,
        client: Client,
    ) -> None:
        self._get_or_create_subscription = get_or_create_subscription
        self._client = client

    async def __call__(
        self, email: Email, billing_period: CheckoutSessionBillingPeriod
    ) -> str:
        """
        :raises SubscriptionActiveInStripeError:
        :raises UnableToCreateCheckoutSessionError:
        """
        subscription = await self._get_or_create_subscription(email)

        if subscription.is_active_in_stripe():
            raise SubscriptionActiveInStripeError

        return await self._client.create_session(
            billing_period, str(subscription.id), subscription.stripe_customer_id
        )
