from pydantic import BaseModel, HttpUrl

from app.application.stripe.enums import CheckoutSessionBillingPeriod


class CustomerRequest(BaseModel):
    customer_external_id: str


class CreateCheckoutSessionRequest(CustomerRequest):
    billing_period: CheckoutSessionBillingPeriod
    success_url: HttpUrl
