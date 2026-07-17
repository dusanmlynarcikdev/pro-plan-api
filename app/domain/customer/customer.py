from uuid import UUID

from app.domain.customer.email import Email


class Customer:
    def __init__(self, id: UUID, email: Email) -> None:
        self._id: UUID = id
        self._email: Email = email
        self._has_pro: bool = False
        self._stripe_id: str | None = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def email(self) -> Email:
        return self._email

    @property
    def has_pro(self) -> bool:
        return self._has_pro

    @property
    def stripe_id(self) -> str | None:
        return self._stripe_id

    def link_stripe_subscription(self, stripe_customer_id: str) -> None:
        self._has_pro = True
        self._stripe_id = stripe_customer_id

    def has_stripe_subscription(self) -> bool:
        return self.has_pro and self.stripe_id is not None

    def deactivate_pro(self) -> None:
        self._has_pro = False
