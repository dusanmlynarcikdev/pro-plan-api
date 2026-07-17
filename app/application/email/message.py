from typing import NamedTuple

from app.domain.customer.email import Email


class Message(NamedTuple):
    recipient: Email
    subject: str
    body: str
