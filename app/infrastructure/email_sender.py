from email.message import EmailMessage
from os import getenv
from smtplib import SMTP

from fastapi import BackgroundTasks

from app.application.email.message import Message

SMTP_DSN = getenv("SMTP_DSN", "")


class EmailSender:
    def __init__(self, queue: BackgroundTasks) -> None:
        self.__queue = queue

    def send(self, message: Message) -> None:
        email = self.__create_email(message)

        self.__queue.add_task(self.__send_email, email)

    @staticmethod
    def __create_email(message: Message) -> EmailMessage:
        email = EmailMessage()
        email["Subject"] = message.subject
        email["To"] = message.recipient.value
        email.set_content(message.body)

        return email

    @staticmethod
    def __send_email(email: EmailMessage) -> None:
        with SMTP(SMTP_DSN) as s:
            s.send_message(email)
