from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid7

from app.domain.subscription.price import Price
from app.domain.subscription.subscription import Subscription


@dataclass(frozen=True, slots=True)
class Payment:
    id: UUID
    subscription_id: UUID
    price: Price
    paid_at: date

    @classmethod
    def from_subscription(cls, subscription: Subscription, today: date) -> Payment:
        return cls(
            uuid7(),
            subscription.id,
            subscription.price,
            today,
        )
