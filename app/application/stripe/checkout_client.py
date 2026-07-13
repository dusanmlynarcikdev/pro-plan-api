from typing import Protocol

from app.application.stripe.enums import BillingPeriod


class CheckoutClient(Protocol):
    async def create_session(
        self,
        billing_period: BillingPeriod,
        client_reference_id: str,
        customer_id: str | None,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        ...
