import logging
from typing import cast
from uuid import UUID

from app.application.stripe.enums import WebhookEventType
from app.application.stripe.webhook.event import Event
from app.domain.customer.customer import Customer
from app.domain.customer.errors import CustomerNotFoundError
from app.domain.customer.repository import CustomerRepository

logger = logging.getLogger(__name__)


class HandleEventUseCase:
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    async def __call__(self, event: Event) -> None:
        match event.type:
            case WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED:
                await self._handle_customer_subscription_deleted(event)
            case WebhookEventType.CHECKOUT_SESSION_COMPLETED:
                await self._handle_checkout_session_completed(event)

    async def _get_customer(self, client_reference_id: str | None) -> Customer | None:
        try:
            customer_id = UUID(client_reference_id)
        except TypeError, ValueError:
            logger.error(
                "Checkout session completed: Invalid client_reference_id: %s",
                client_reference_id,
            )
            return None

        try:
            return await self._repository.get(customer_id)
        except CustomerNotFoundError:
            logger.error(
                "Checkout session completed: Customer not found for id: %s",
                customer_id,
            )
            return None

    async def _handle_customer_subscription_deleted(self, event: Event) -> None:
        customer_id = cast(str, event.data.get("customer"))
        customer = await self._repository.find_one_by_stripe_id(customer_id)

        if customer is None:
            logger.error(
                "Customer subscription deleted: Customer not found for id: %s",
                customer_id,
            )
            return

        customer.deactivate_pro()

        await self._repository.update(customer)
        await self._repository.commit()

    async def _handle_checkout_session_completed(self, event: Event) -> None:
        customer = await self._get_customer(event.data.get("client_reference_id"))

        if customer is None:
            return

        customer.link_stripe_subscription(cast(str, event.data.get("customer")))

        await self._repository.update(customer)
        await self._repository.commit()
