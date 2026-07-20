from app.application.stripe.billing_portal.client import Client
from app.application.stripe.errors import CustomerIsNotLinkedToStripeError
from app.domain.customer.repository import CustomerRepository


class CreateSessionUseCase:
    def __init__(self, client: Client, repository: CustomerRepository) -> None:
        self._client = client
        self._repository = repository

    async def __call__(self, external_customer_id: str) -> str:
        """
        :raises CustomerIsNotLinkedToStripeError:
        :raises CustomerNotFound:
        :raises UnableToCreateBillingPortalSessionError:
        """
        customer = await self._repository.get_by_external_id(external_customer_id)

        if customer.stripe_id is None:
            raise CustomerIsNotLinkedToStripeError

        return await self._client.create_session(customer.stripe_id)
