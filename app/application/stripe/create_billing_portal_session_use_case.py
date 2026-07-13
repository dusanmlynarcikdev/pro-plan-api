from app.application.stripe.billing_portal_client import BillingPortalClient
from app.domain.subscription.repository import SubscriptionRepository


class CreateBillingPortalSessionUseCase:
    def __init__(
        self, client: BillingPortalClient, repository: SubscriptionRepository
    ) -> None:
        self._client = client
        self._repository = repository

    async def __call__(self, stripe_customer_id: str) -> str:
        """
        :raises UnableToCreateBillingPortalSessionError:
        """
        return await self._client.create_session(stripe_customer_id)
