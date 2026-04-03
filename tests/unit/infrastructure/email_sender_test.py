from email.message import EmailMessage
from smtplib import SMTP
from unittest.mock import MagicMock, Mock, patch

from fastapi import BackgroundTasks

from app.application.email.message import Message
from app.domain.subscription.email import Email
from app.infrastructure.email_sender import SMTP_DSN, EmailSender


def test_send() -> None:
    background_tasks = Mock(BackgroundTasks)

    EmailSender(background_tasks).send(
        Message(Email("john@doe.com"), "subject", "body")
    )

    background_tasks.add_task.assert_called_once()

    callback, email = background_tasks.add_task.call_args.args

    assert callback == getattr(EmailSender, "_EmailSender__send_email")

    assert isinstance(email, EmailMessage)
    assert email["To"] == "john@doe.com"
    assert email["Subject"] == "subject"
    assert email.get_content().strip() == "body"


def test_send_email() -> None:
    email = EmailMessage()
    email["To"] = "john@doe.com"
    email["Subject"] = "subject"
    email.set_content("body")

    smtp = MagicMock(SMTP)
    smtp_client = smtp.return_value.__enter__.return_value

    with patch("app.infrastructure.email_sender.SMTP", smtp):
        getattr(EmailSender, "_EmailSender__send_email")(email)

    smtp.assert_called_once_with(SMTP_DSN)
    smtp_client.send_message.assert_called_once_with(email)
