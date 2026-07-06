from email.message import EmailMessage
from unittest.mock import MagicMock, Mock, patch

from aiosmtplib import SMTP
from fastapi import BackgroundTasks
from pydantic import AnyUrl, NameEmail

from app.application.email.message import Message
from app.domain.subscription.email import Email
from app.infrastructure.email_sender import EmailSender


def test_send() -> None:
    background_tasks = Mock(BackgroundTasks)

    EmailSender(
        background_tasks,
        NameEmail("Acme", "noreply@acme.test"),
        AnyUrl("smtp://john:secret@example.com:465"),
    ).send(Message(Email("john@doe.com"), "subject", "body"))

    background_tasks.add_task.assert_called_once()

    callback, email = background_tasks.add_task.call_args.args

    assert callback.__func__ is getattr(EmailSender, "_EmailSender__send_email")

    assert isinstance(email, EmailMessage)
    assert email["From"] == "Acme <noreply@acme.test>"
    assert email["To"] == "john@doe.com"
    assert email["Subject"] == "subject"
    assert email.get_content().strip() == "body"


async def test_send_email() -> None:
    email = EmailMessage()
    email["To"] = "john@doe.com"
    email["Subject"] = "subject"
    email.set_content("body")

    smtp = MagicMock(SMTP)
    smtp_client = smtp.return_value.__aenter__.return_value

    sender = EmailSender(
        Mock(BackgroundTasks),
        NameEmail("Acme", "noreply@acme.test"),
        AnyUrl("smtp://john:secret@example.com:465"),
    )

    with patch("app.infrastructure.email_sender.SMTP", smtp):
        await getattr(sender, "_EmailSender__send_email")(email)

    smtp.assert_called_once_with(
        hostname="example.com",
        port=465,
        use_tls=True,
    )
    smtp_client.login.assert_called_once_with("john", "secret")
    smtp_client.send_message.assert_called_once_with(email)
