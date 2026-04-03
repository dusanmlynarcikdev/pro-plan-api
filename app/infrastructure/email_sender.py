from datetime import date
from email.message import EmailMessage
from os import getenv
from smtplib import SMTP

from fastapi import BackgroundTasks

from app.domain.subscription.email import Email

SMTP_DSN = getenv("SMTP_DSN", "")


class EmailSender:
    def __init__(self, queue: BackgroundTasks) -> None:
        self.__queue = queue

    def send_renewal_confirmation(self, recipient: Email, expires_at: date) -> None:
        email = self.__create_email(
            recipient,
            "Subscription renewed",
            f"Subscription renewed. Expires on {expires_at.strftime('%b %-d, %Y')}.",
        )

        self.__queue.add_task(self.__send_email, email)

    @staticmethod
    def __create_email(recipient: Email, subject: str, content: str) -> EmailMessage:
        message = EmailMessage()
        message["Subject"] = subject
        message["To"] = recipient.value
        message.set_content(content)

        return message

    @staticmethod
    def __send_email(email: EmailMessage) -> None:
        with SMTP(SMTP_DSN) as s:
            s.send_message(email)
