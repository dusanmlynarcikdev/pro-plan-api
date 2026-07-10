from typing import Protocol


class CheckoutClient(Protocol):
    async def create_session(self, price_id: str, client_reference_id: str) -> str:
        """
        :raises CheckoutError:
        """
        ...
