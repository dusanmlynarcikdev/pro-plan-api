from typing import Protocol
from uuid import UUID

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription


class SubscriptionRepository(Protocol):
    async def add(self, subscription: Subscription) -> None: ...

    async def commit(self) -> None: ...

    async def find_one_by_email(self, email: Email) -> Subscription | None: ...

    async def find_one_by_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Subscription | None: ...

    async def get(self, id: UUID) -> Subscription:
        """
        :raises SubscriptionNotFound:
        """
        ...

    async def get_by_email(self, email: Email) -> Subscription:
        """
        :raises SubscriptionNotFound:
        """
        ...

    async def update(self, subscription: Subscription) -> None: ...
