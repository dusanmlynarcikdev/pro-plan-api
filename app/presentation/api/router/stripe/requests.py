from pydantic import BaseModel

from app.infrastructure.stripe.checkout.billing_period import BillingPeriod


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
