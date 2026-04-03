from datetime import date

from app.domain.subscription.email import Email
from app.domain.subscription.email_sender import EmailSender
from app.domain.subscription.repository import SubscriptionRepository


class RenewalSubscriptionUseCase:
    def __init__(
        self, email_sender: EmailSender, repository: SubscriptionRepository
    ) -> None:
        self.__email_sender: EmailSender = email_sender
        self.__repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> None:
        """
        :raises SubscriptionNotFound:
        """
        subscription = await self.__repository.get_one_by_email(email)

        expires_at = subscription.renew(date.today())
        await self.__repository.update(subscription)

        self.__email_sender.send_renewal_confirmation(subscription.email, expires_at)
