from email.message import EmailMessage
from os import getenv
from urllib.parse import urlparse

from aiosmtplib import SMTP
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
    async def __send_email(message: EmailMessage) -> None:
        parsed_dsn = urlparse(SMTP_DSN)

        async with SMTP(
            hostname=parsed_dsn.hostname,
            port=parsed_dsn.port,
            use_tls=parsed_dsn.port == 465,
        ) as client:
            if parsed_dsn.username and parsed_dsn.password:
                await client.login(parsed_dsn.username, parsed_dsn.password)

            await client.send_message(message)
