from uuid import UUID


class Customer:
    def __init__(self, id: UUID, external_id: str) -> None:
        self._id = id
        self._external_id = external_id
        self._stripe_id: str | None = None
        self._stripe_product_id: str | None = None

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
    def can_access_stripe_billing_portal(self) -> bool:
        return self.stripe_id is not None

    def link_subscription(
        self, stripe_customer_id: str, stripe_product_id: str
    ) -> None:
        self._stripe_id = stripe_customer_id
        self._stripe_product_id = stripe_product_id

    def has_subscription(self) -> bool:
        return self.stripe_id is not None and self.stripe_product_id is not None

    def remove_subscription(self) -> None:
        self._stripe_product_id = None
