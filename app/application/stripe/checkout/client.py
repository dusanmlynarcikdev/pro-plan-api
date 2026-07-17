from typing import Protocol

from app.application.stripe.enums import CheckoutSessionBillingPeriod


class Client(Protocol):
    async def create_session(
        self,
        billing_period: CheckoutSessionBillingPeriod,
        client_reference_id: str,
        customer_id: str | None,
        success_url: str,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        ...
