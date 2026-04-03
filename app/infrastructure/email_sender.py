from email.message import EmailMessage
from os import getenv
from smtplib import SMTP

from fastapi import BackgroundTasks

from app.application.email.message import Message

SMTP_DSN = getenv("SMTP_DSN", "")


class EmailSender:
    def __init__(self, background_tasks: BackgroundTasks) -> None:
        self.__background_tasks = background_tasks

    def send(self, message: Message) -> None:
        email = self.__create_email(message)

        self.__background_tasks.add_task(self.__send_email, email)

    @staticmethod
    def __create_email(message: Message) -> EmailMessage:
        email = EmailMessage()
        email["To"] = message.recipient.value
        email["Subject"] = message.subject
        email.set_content(message.body)

        return email

    @staticmethod
    def __send_email(email: EmailMessage) -> None:
        with SMTP(SMTP_DSN) as s:
            s.send_message(email)
