from datetime import datetime
from typing import Any, NamedTuple

from pydantic import BaseModel


class Event(NamedTuple):
    type: str
    data: dict[str, Any]


class SubscriptionItemPrice(BaseModel):
    product: str


class SubscriptionItem(BaseModel):
    current_period_end: datetime
    price: SubscriptionItemPrice


class SubscriptionItems(BaseModel):
    data: list[SubscriptionItem]


class Subscription(BaseModel):
    cancel_at: datetime | None
    customer: str
    items: SubscriptionItems
    metadata: dict[str, str]
    status: str
