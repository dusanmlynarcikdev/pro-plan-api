from datetime import date

from app.application.email.message import Message
from app.application.email.sender import Sender
from app.domain.subscription.email import Email
from app.domain.subscription.repository import SubscriptionRepository


class RenewSubscriptionUseCase:
    def __init__(
        self, email_sender: Sender, repository: SubscriptionRepository
    ) -> None:
        self.__email_sender: Sender = email_sender
        self.__repository: SubscriptionRepository = repository

    async def __call__(self, email: Email) -> None:
        """
        :raises SubscriptionNotFound:
        """
        subscription = await self.__repository.get_one_by_email(email)

        expires_at = subscription.renew(date.today())
        await self.__repository.update(subscription)

        self.__send_confirmation_email(subscription.email, expires_at)

    def __send_confirmation_email(self, recipient: Email, expires_at: date) -> None:
        message = Message(
            recipient,
            "Subscription renewed",
            f"Subscription renewed. Expires on {expires_at.strftime('%b %-d, %Y')}.",
        )

        self.__email_sender.send(message)
