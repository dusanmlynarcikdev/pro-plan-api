from pydantic import BaseModel

from app.application.stripe.enums import BillingPeriod


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
