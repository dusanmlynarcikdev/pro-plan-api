from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.subscription import Subscription


class GetSubscriptionUseCase:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self.__repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> Subscription:
        """
        :raises SubscriptionNotFound:
        """
        return await self.__repository.get_one_by_email(email)
