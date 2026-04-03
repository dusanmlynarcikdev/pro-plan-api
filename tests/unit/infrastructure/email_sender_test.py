from email.message import EmailMessage
from unittest.mock import Mock

from fastapi import BackgroundTasks

from app.application.email.message import Message
from app.domain.subscription.email import Email
from app.infrastructure.email_sender import EmailSender


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
