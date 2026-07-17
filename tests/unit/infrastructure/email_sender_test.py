from email.message import EmailMessage
from unittest.mock import MagicMock, patch

from aiosmtplib import SMTP
from pydantic import AnyUrl, NameEmail

from app.application.email.message import Message
from app.domain.customer.email import Email
from app.infrastructure import email_sender as email_sender_module
from app.infrastructure.email_sender import EmailSender


async def test_send() -> None:
    email_sender = EmailSender(
        NameEmail("Acme", "noreply@acme.test"),
        AnyUrl("smtp://john:secret@example.com:465"),
    )

    smtp = MagicMock(SMTP)
    smtp_client = smtp.return_value.__aenter__.return_value

    with patch.object(email_sender_module, "SMTP", smtp):
        await email_sender.send(Message(Email("john@doe.com"), "subject", "body"))

    smtp.assert_called_once_with(hostname="example.com", port=465, use_tls=True)

    smtp_client.login.assert_called_once_with("john", "secret")
    smtp_client.send_message.assert_called_once()

    email = smtp_client.send_message.call_args.args[0]
    assert isinstance(email, EmailMessage)
    assert email["From"] == "Acme <noreply@acme.test>"
    assert email["To"] == "john@doe.com"
    assert email["Subject"] == "subject"
    assert email.get_content().strip() == "body"
