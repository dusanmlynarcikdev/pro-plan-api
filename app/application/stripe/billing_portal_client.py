from typing import Protocol


class BillingPortalClient(Protocol):
    async def create_session(
        self,
        customer_id: str,
    ) -> str:
        """
        :raises UnableToCreateBillingPortalSessionError:
        """
        ...
