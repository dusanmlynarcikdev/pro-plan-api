from dataclasses import dataclass
from datetime import date
from uuid import UUID

from app.domain.subscription.price import Price


@dataclass(frozen=True, slots=True)
class Payment:
    id: UUID
    subscription_id: UUID
    price: Price
    paid_at: date
