from typing import Protocol


class Client(Protocol):
    async def create_session(
        self,
        client_reference_id: str,
        customer_id: str | None,
        price_id: str,
        success_url: str,
    ) -> str:
        """
        :raises UnableToCreateCheckoutSessionError:
        """
        ...
