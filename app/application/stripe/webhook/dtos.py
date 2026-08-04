from typing import Any, NamedTuple

from pydantic import AwareDatetime, BaseModel


class Event(NamedTuple):
    type: str
    data: dict[str, Any]


class SubscriptionItemPrice(BaseModel):
    product: str


class SubscriptionItem(BaseModel):
    current_period_end: AwareDatetime
    price: SubscriptionItemPrice


class SubscriptionItems(BaseModel):
    data: list[SubscriptionItem]


class Subscription(BaseModel):
    cancel_at: AwareDatetime | None
    customer: str
    items: SubscriptionItems
    metadata: dict[str, str]
    status: str
