from datetime import datetime
from uuid import UUID

from app.domain.customer.enums import StripeSubscriptionActiveStatus


class Customer:
    def __init__(self, id: UUID, external_id: str) -> None:
        self._id = id
        self._external_id = external_id
        self._stripe_id: str | None = None
        self._stripe_subscription_product_id: str | None = None
        self._stripe_subscription_status: str | None = None
        self._stripe_subscription_period_end_at: datetime | None = None
        self._stripe_subscription_cancel_at: datetime | None = None

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
    def stripe_subscription_product_id(self) -> str | None:
        return self._stripe_subscription_product_id

    @property
    def stripe_subscription_status(self) -> str | None:
        return self._stripe_subscription_status

    @property
    def stripe_subscription_period_end_at(self) -> datetime | None:
        return self._stripe_subscription_period_end_at

    @property
    def stripe_subscription_cancel_at(self) -> datetime | None:
        return self._stripe_subscription_cancel_at

    def can_access_stripe_billing_portal(self) -> bool:
        return self.stripe_id is not None

    def is_stripe_subscription_active(self) -> bool:
        return self.stripe_subscription_status in StripeSubscriptionActiveStatus

    def is_stripe_subscription_trial(self) -> bool:
        return (
            self.stripe_subscription_status == StripeSubscriptionActiveStatus.TRIALING
        )

    def is_stripe_subscription_cancelling(self) -> bool:
        return self._stripe_subscription_cancel_at is not None

    def set_stripe(
        self,
        customer_id: str,
        subscription_product_id: str,
        subscription_status: str,
        subscription_period_end_at: datetime,
        subscription_cancel_at: datetime | None,
    ) -> None:
        self._stripe_id = customer_id
        self._stripe_subscription_product_id = subscription_product_id
        self._stripe_subscription_status = subscription_status
        self._stripe_subscription_period_end_at = subscription_period_end_at
        self._stripe_subscription_cancel_at = subscription_cancel_at
