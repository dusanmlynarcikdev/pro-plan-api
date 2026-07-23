import logging

from app.application.stripe.billing_portal.client import Client
from app.application.stripe.errors import (
    CustomerIsNotLinkedToStripeError,
    UnableToCreateBillingPortalSessionError,
)
from app.domain.customer.repository import CustomerRepository

logger = logging.getLogger(__name__)


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

        if not customer.can_access_stripe_billing_portal:
            raise CustomerIsNotLinkedToStripeError

        if not customer.stripe_id:
            raise ValueError("Stripe customer ID is missing")

        try:
            return await self._client.create_session(customer.stripe_id)
        except UnableToCreateBillingPortalSessionError as e:
            logger.error(e.__cause__)
            raise
