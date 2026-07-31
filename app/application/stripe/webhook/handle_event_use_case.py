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
    def __init__(self, repository: CustomerRepository) -> None:
        self._repository = repository

    async def __call__(self, event: Event) -> None:
        match event.type:
            case WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED:
                await self._handle_customer_subscription_created(event)
            case WebhookEventType.CUSTOMER_SUBSCRIPTION_UPDATED:
                await self._handle_customer_subscription_updated(event)
            case WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED:
                await self._handle_customer_subscription_deleted(event)

    async def _get_customer_by_metadata(self, metadata: dict[str, str]) -> Customer:
        customer_id = metadata.get(SubscriptionMetadataKey.CUSTOMER_ID)

        try:
            customer_id = UUID(customer_id)
        except TypeError, ValueError:
            raise ValueError(f"Invalid metadata customer id: {customer_id}")

        try:
            return await self._repository.get(customer_id)
        except CustomerNotFoundError:
            raise ValueError(f"Customer not found for id: {customer_id}")

    async def _handle_customer_subscription_created(self, event: Event) -> None:
        try:
            customer = await self._get_customer_by_metadata(
                cast(dict, event.data.get("metadata"))
            )
        except ValueError as e:
            logger.error(f"{WebhookEventType.CUSTOMER_SUBSCRIPTION_CREATED}: {e}")
            return

        items = cast(list[dict], cast(dict, event.data.get("items")).get("data"))

        customer.link_subscription(
            cast(str, event.data.get("customer")),
            cast(str, cast(dict, items[0].get("price")).get("product")),
        )

        await self._repository.update(customer)
        await self._repository.commit()

    async def _handle_customer_subscription_updated(self, event: Event) -> None:
        customer_id = cast(str, event.data.get("customer"))

        try:
            customer = await self._repository.get_by_stripe_id(customer_id)
        except CustomerNotFoundError:
            logger.error(
                f"{WebhookEventType.CUSTOMER_SUBSCRIPTION_UPDATED}: "
                f"Customer not found for id: {customer_id}"
            )
            return

        await self._link_subscription(customer, event)

    async def _handle_customer_subscription_deleted(self, event: Event) -> None:
        customer_id = cast(str, event.data.get("customer"))
        customer = await self._repository.find_one_by_stripe_id(customer_id)

        if customer is None:
            logger.error(
                f"{WebhookEventType.CUSTOMER_SUBSCRIPTION_DELETED}: "
                f"Customer not found for id: {customer_id}",
            )
            return

        customer.remove_subscription()

        await self._repository.update(customer)
        await self._repository.commit()

    async def _link_subscription(self, customer: Customer, event: Event) -> None:
        items = cast(list[dict], cast(dict, event.data.get("items")).get("data"))

        customer.link_subscription(
            cast(str, event.data.get("customer")),
            cast(str, cast(dict, items[0].get("price")).get("product")),
        )

        await self._repository.update(customer)
        await self._repository.commit()
