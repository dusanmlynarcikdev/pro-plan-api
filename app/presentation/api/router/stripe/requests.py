from pydantic import HttpUrl

from app.application.stripe.enums import CheckoutSessionBillingPeriod
from app.presentation.api.requests import BaseRequest


class CreateCheckoutSessionRequest(BaseRequest):
    billing_period: CheckoutSessionBillingPeriod
    customer_external_id: str
    success_url: HttpUrl
