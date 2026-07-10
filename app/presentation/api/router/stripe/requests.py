from pydantic import BaseModel

from app.infrastructure.stripe.client.billing_period import BillingPeriod


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
