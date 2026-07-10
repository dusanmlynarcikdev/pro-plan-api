from app.application.stripe.checkout_client import CheckoutClient
from app.application.stripe.enums import BillingPeriod
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)
from app.domain.subscription.email import Email


class CreateCheckoutSessionUseCase:
    def __init__(
        self,
        get_or_create_subscription: GetOrCreateSubscriptionUseCase,
        checkout_client: CheckoutClient,
        price_id_monthly: str,
        price_id_yearly: str,
    ) -> None:
        self._get_or_create_subscription = get_or_create_subscription
        self._checkout_client = checkout_client
        self._price_id_monthly = price_id_monthly
        self._price_id_yearly = price_id_yearly

    async def __call__(self, email: Email, billing_period: BillingPeriod) -> str:
        """
        :raises CheckoutError:
        """
        subscription = await self._get_or_create_subscription(email)
        price_id = self._resolve_price_id(billing_period)

        return await self._checkout_client.create_session(
            price_id, str(subscription.id)
        )

    def _resolve_price_id(self, billing_period: BillingPeriod) -> str:
        match billing_period:
            case BillingPeriod.MONTHLY:
                return self._price_id_monthly
            case BillingPeriod.YEARLY:
                return self._price_id_yearly
