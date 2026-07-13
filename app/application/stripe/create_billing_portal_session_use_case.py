from app.application.stripe.billing_portal_client import BillingPortalClient
from app.application.stripe.errors import StripeCustomerIdIsMissingError
from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository


class CreateBillingPortalSessionUseCase:
    def __init__(
        self, client: BillingPortalClient, repository: SubscriptionRepository
    ) -> None:
        self._client = client
        self._repository = repository

    async def __call__(self, email: Email) -> str:
        """
        :raises StripeCustomerIdIsMissingError:
        :raises SubscriptionNotFound:
        :raises UnableToCreateBillingPortalSessionError:
        """
        subscription = await self._repository.get_one_by_email(email)

        if subscription.stripe_customer_id is None:
            raise StripeCustomerIdIsMissingError

        return await self._client.create_session(subscription.stripe_customer_id)
