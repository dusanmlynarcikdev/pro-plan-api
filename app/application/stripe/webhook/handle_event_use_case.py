import logging
from typing import cast
from uuid import UUID

from app.application.stripe.enums import SubscriptionMetadataKey, WebhookEventType
from app.application.stripe.webhook.event import Event
from app.domain.customer.customer import Customer
from app.domain.customer.errors import CustomerNotFoundError
from app.domain.customer.repository import CustomerRepository

logger = logging.getLogger(__name__)


class HandleEventUseCase:
    def __init__(self, customer_repository: CustomerRepository) -> None:
        self._customer_repository = customer_repository

    async def __call__(self, event: Event) -> None:
        match event.type:
            case (
                WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED
                | WebhookEventType.CUSTOMER_SUBSCRIPTION_UPDATED
                | WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED
            ):
                await self._handle_customer_subscription(event)

    async def _get_customer(self, metadata: dict[str, str]) -> Customer:
        customer_id = metadata.get(key := SubscriptionMetadataKey.CUSTOMER_ID)

        try:
            customer_id = UUID(customer_id)
        except TypeError, ValueError:
            raise ValueError(f"Invalid metadata {key}: {customer_id}")

        try:
            return await self._customer_repository.get(customer_id)
        except CustomerNotFoundError as e:
            raise ValueError(f"{e}: {customer_id}")

    async def _handle_customer_subscription(self, event: Event) -> None:
        metadata = cast(dict, event.data.get("metadata"))

        try:
            customer = await self._get_customer(metadata)
        except ValueError as e:
            logger.error(f"{event.type}: {e}")
            return

        await self._update_customer(customer, event)

    async def _update_customer(self, customer: Customer, event: Event) -> None:
        items = cast(list[dict], cast(dict, event.data.get("items")).get("data"))

        customer.set_stripe(
            cast(str, event.data.get("customer")),
            cast(str, cast(dict, items[0].get("price")).get("product")),
            cast(str, event.data.get("status")),
        )

        await self._customer_repository.update(customer)
        await self._customer_repository.commit()
