from app.application.stripe.billing_portal.client import Client


class CreateSessionUseCase:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def __call__(self, stripe_customer_id: str) -> str:
        """
        :raises UnableToCreateBillingPortalSessionError:
        """
        return await self._client.create_session(stripe_customer_id)
