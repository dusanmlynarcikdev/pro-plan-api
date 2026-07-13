from pydantic import BaseModel

from app.application.stripe.enums import BillingPeriod


class CreateBillingPortalSessionRequest(BaseModel):
    email: str


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
