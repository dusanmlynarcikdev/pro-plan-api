from uuid import UUID


class Customer:
    def __init__(self, id: UUID, external_id: str) -> None:
        self._id = id
        self._external_id = external_id
        self._has_pro: bool = False
        self._stripe_id: str | None = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def external_id(self) -> str:
        return self._external_id

    @property
    def has_pro(self) -> bool:
        return self._has_pro

    @property
    def stripe_id(self) -> str | None:
        return self._stripe_id

    @property
    def can_access_stripe_billing_portal(self) -> bool:
        return self.stripe_id is not None

    def link_stripe_subscription(self, stripe_customer_id: str) -> None:
        self._has_pro = True
        self._stripe_id = stripe_customer_id

    def has_stripe_subscription(self) -> bool:
        return self.has_pro and self.stripe_id is not None

    def deactivate_pro(self) -> None:
        self._has_pro = False
