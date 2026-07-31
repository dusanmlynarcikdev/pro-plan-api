from uuid import UUID


class Customer:
    def __init__(self, id: UUID, external_id: str) -> None:
        self._id = id
        self._external_id = external_id
        self._stripe_id: str | None = None
        self._stripe_product_id: str | None = None
        self._stripe_subscription_status: str | None = None

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def external_id(self) -> str:
        return self._external_id

    @property
    def stripe_id(self) -> str | None:
        return self._stripe_id

    @property
    def stripe_product_id(self) -> str | None:
        return self._stripe_product_id

    @property
    def stripe_subscription_status(self) -> str | None:
        return self._stripe_subscription_status

    @property
    def can_access_stripe_billing_portal(self) -> bool:
        return self.stripe_id is not None

    @property
    def has_active_subscription(self) -> bool:
        return self.stripe_subscription_status in ("active", "past_due")

    def set_stripe(
        self, customer_id: str, subscription_product_id: str, subscription_status: str
    ) -> None:
        self._stripe_id = customer_id
        self._stripe_product_id = subscription_product_id
        self._stripe_subscription_status = subscription_status
