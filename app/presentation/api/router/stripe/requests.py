from pydantic import HttpUrl, PositiveInt

from app.presentation.api.requests import BaseRequest


class CreateCheckoutSessionRequest(BaseRequest):
    customer_external_id: str
    stripe_price_id: str
    success_url: HttpUrl
    trial_days: PositiveInt | None = None
    automatic_tax: bool = False
    business_customers: bool = False
