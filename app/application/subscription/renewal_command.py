from datetime import date

from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository


class RenewalSubscriptionCommand:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self.__repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> None:
        """
        :raises SubscriptionNotFound:
        """
        subscription = await self.__repository.get_one_by_email(email)

        subscription.renew(date.today())

        await self.__repository.update(subscription)
