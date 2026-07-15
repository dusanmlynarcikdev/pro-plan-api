from app.application.stripe.billing_portal.client import Client
from app.domain.subscription.repository import SubscriptionRepository


class CreateSessionUseCase:
    def __init__(self, client: Client, repository: SubscriptionRepository) -> None:
        self._client = client
        self._repository = repository

    async def __call__(self, stripe_customer_id: str) -> str:
        """
        :raises UnableToCreateBillingPortalSessionError:
        """
        return await self._client.create_session(stripe_customer_id)
