from datetime import datetime

from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    stripe: CustomerStripeResponse


class CustomerStripeResponse(BaseResponse):
    can_access_billing_portal: bool
    subscription: CustomerStripeSubscriptionResponse | None


class CustomerStripeSubscriptionResponse(BaseResponse):
    is_active: bool
    is_trial: bool
    product_id: str
    current_period_end_at: datetime
    cancel_at: datetime | None
