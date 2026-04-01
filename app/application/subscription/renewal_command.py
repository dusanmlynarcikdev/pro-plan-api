from datetime import date

from app.domain.payment.payment import Payment
from app.domain.payment.repository import PaymentRepository
from app.domain.subscription.email import Email
from app.domain.subscription.errors import SubscriptionNotFound
from app.domain.subscription.repository import SubscriptionRepository


class RenewalSubscriptionCommand:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        subscription_repository: SubscriptionRepository,
    ) -> None:
        self.__payment_repository: PaymentRepository = payment_repository
        self.__subscription_repository: SubscriptionRepository = subscription_repository

    async def __call__(self, email: Email) -> None:
        """
        :raises SubscriptionNotFound:
        """
        subscription = await self.__subscription_repository.find_one_by_email(email)

        if subscription is None:
            raise SubscriptionNotFound()

        today = date.today()

        subscription.renew(today)
        await self.__subscription_repository.update(subscription)

        await self.__payment_repository.add(
            Payment.from_subscription(subscription, today)
        )
