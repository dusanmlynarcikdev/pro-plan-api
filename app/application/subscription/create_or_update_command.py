from uuid import uuid7

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.subscription import Subscription


class CreateOrUpdateSubscriptionCommand:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self.__repository: SubscriptionRepository = repository

    async def __call__(self, email: Email, period: Period) -> None:
        subscription = await self.__repository.find_one_by_email(email)

        if subscription is None:
            await self.__repository.add(Subscription(uuid7(), email, period))
            return

        subscription.period = period
        await self.__repository.update(subscription)
