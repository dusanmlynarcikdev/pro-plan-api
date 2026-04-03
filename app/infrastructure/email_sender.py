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
        _message = self.__create_message(message)

        self.__background_tasks.add_task(self.__send_email, _message)

    @staticmethod
    def __create_message(message: Message) -> EmailMessage:
        _message = EmailMessage()
        _message["To"] = message.recipient.value
        _message["Subject"] = message.subject
        _message.set_content(message.body)

        return _message

    @staticmethod
    def __send_email(message: EmailMessage) -> None:
        with SMTP(SMTP_DSN) as s:
            s.send_message(message)
