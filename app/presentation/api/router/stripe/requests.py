from pydantic import BaseModel

from app.application.stripe.billing_period import BillingPeriod


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
