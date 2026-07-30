from typing import Protocol


class Client(Protocol):
    async def create_session(
        self,
        customer_id: str,
        stripe_customer_id: str | None,
        price_id: str,
        success_url: str,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        ...
