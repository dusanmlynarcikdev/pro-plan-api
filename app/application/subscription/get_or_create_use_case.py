from uuid import uuid7

from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.subscription import Subscription


class GetOrCreateUseCase:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self._repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> Subscription:
        subscription = await self._repository.find_one_by_email(email)

        if subscription is None:
            subscription = Subscription(uuid7(), email)
            await self._repository.add(subscription)
            await self._repository.commit()

        return subscription
