from enum import StrEnum

from pydantic import BaseModel


class SubscriptionPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    period: SubscriptionPeriod
