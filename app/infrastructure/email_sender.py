from email.message import EmailMessage

from aiosmtplib import SMTP
from aiosmtplib.smtp import SMTP_TLS_PORT
from fastapi import BackgroundTasks
from pydantic import AnyUrl, NameEmail

from app.application.email.message import Message


class EmailSender:
    def __init__(
        self,
        background_tasks: BackgroundTasks,
        email_sender: NameEmail,
        smtp_dsn: AnyUrl,
    ) -> None:
        self._background_tasks = background_tasks
        self._email_sender = email_sender
        self._smtp_dsn = smtp_dsn

    def send(self, message: Message) -> None:
        _message = self.__create_message(message)

        self._background_tasks.add_task(self.__send_email, _message)

    def __create_message(self, message: Message) -> EmailMessage:
        _message = EmailMessage()
        _message["From"] = str(self._email_sender)
        _message["To"] = message.recipient.value
        _message["Subject"] = message.subject
        _message.set_content(message.body)

        return _message

    async def __send_email(self, message: EmailMessage) -> None:
        async with SMTP(
            hostname=self._smtp_dsn.host,
            port=self._smtp_dsn.port,
            use_tls=self._smtp_dsn.port == SMTP_TLS_PORT,
        ) as client:
            if self._smtp_dsn.username and self._smtp_dsn.password:
                await client.login(self._smtp_dsn.username, self._smtp_dsn.password)

            await client.send_message(message)
