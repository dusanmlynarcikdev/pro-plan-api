from pydantic import BaseModel, HttpUrl

from app.application.stripe.enums import CheckoutSessionBillingPeriod


class CreateBillingPortalSessionRequest(BaseModel):
    stripe_customer_id: str


class CreateCheckoutSessionRequest(BaseModel):
    billing_period: CheckoutSessionBillingPeriod
    customer_external_id: str
    success_url: HttpUrl
