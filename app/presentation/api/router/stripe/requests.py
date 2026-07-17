from pydantic import BaseModel

from app.application.stripe.enums import CheckoutSessionBillingPeriod


class CreateBillingPortalSessionRequest(BaseModel):
    stripe_customer_id: str


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: CheckoutSessionBillingPeriod
