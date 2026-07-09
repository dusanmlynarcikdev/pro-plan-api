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

        await self.__repository.update(subscription)
        await self.__repository.commit()

        self.__send_confirmation_email(subscription.email)

    def __send_confirmation_email(self, recipient: Email) -> None:
        message = Message(
            recipient,
            "Subscription renewed",
            "Your subscription has been successfully renewed.",
        )

        self.__email_sender.send(message)
