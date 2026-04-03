from datetime import date
from typing import Protocol

from app.domain.subscription.email import Email


class EmailSender(Protocol):
    def send_renewal_confirmation(self, recipient: Email, expires_at: date) -> None: ...
