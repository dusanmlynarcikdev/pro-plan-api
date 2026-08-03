from typing import Any, NamedTuple

from pydantic import BaseModel


class Event(NamedTuple):
    type: str
    data: dict[str, Any]


class SubscriptionItemPrice(BaseModel):
    product: str


class SubscriptionItem(BaseModel):
    price: SubscriptionItemPrice


class SubscriptionItems(BaseModel):
    data: list[SubscriptionItem]


class Subscription(BaseModel):
    customer: str
    items: SubscriptionItems
    metadata: dict[str, str]
    status: str
