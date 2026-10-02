from typing import Protocol


class Client(Protocol):
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
        ...
