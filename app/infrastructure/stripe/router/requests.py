from enum import StrEnum

from pydantic import BaseModel


class BillingPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
