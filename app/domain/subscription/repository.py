from typing import Protocol

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription


class SubscriptionRepository(Protocol):
    async def add(self, subscription: Subscription) -> None: ...

    async def find_one_by_email(self, email: Email) -> Subscription | None: ...

    async def update(self, subscription: Subscription) -> None: ...
