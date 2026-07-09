from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository
from app.domain.subscription.subscription import Subscription


class GetUseCase:
    def __init__(self, repository: SubscriptionRepository) -> None:
        self._repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> Subscription:
        """
        :raises SubscriptionNotFound:
        """
        return await self._repository.get_one_by_email(email)
