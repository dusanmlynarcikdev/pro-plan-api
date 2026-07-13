from uuid import UUID

from app.domain.subscription.email import Email


class Subscription:
    def __init__(self, id: UUID, email: Email) -> None:
        self._id: UUID = id
        self._email: Email = email
        self._is_active: bool = False
        self._stripe_customer_id: str | None = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def stripe_customer_id(self) -> str | None:
        return self._stripe_customer_id

    def activate(self) -> None:
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False
