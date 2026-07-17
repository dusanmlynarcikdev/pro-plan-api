from uuid import UUID

from app.domain.customer.email import Email


class Customer:
    def __init__(self, id: UUID, email: Email) -> None:
        self._id: UUID = id
        self._email: Email = email
        self._has_pro: bool = False
        self.stripe_id: str | None = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def has_pro(self) -> bool:
        return self._has_pro

    def has_stripe_subscription(self) -> bool:
        return self.has_pro and self.stripe_id is not None

    def activate_pro(self) -> None:
        self._has_pro = True

    def deactivate_pro(self) -> None:
        self._has_pro = False
