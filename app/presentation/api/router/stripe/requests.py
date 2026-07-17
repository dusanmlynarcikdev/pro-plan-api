from pydantic import BaseModel

from app.application.stripe.enums import CheckoutSessionBillingPeriod


class CreateBillingPortalSessionRequest(BaseModel):
    stripe_customer_id: str


class CreateCheckoutSessionRequest(BaseModel):
    billing_period: CheckoutSessionBillingPeriod
    customer_external_id: str
