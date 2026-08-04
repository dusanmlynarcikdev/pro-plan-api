from datetime import datetime

from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    stripe: CustomerStripeResponse


class CustomerStripeResponse(BaseResponse):
    can_access_billing_portal: bool
    subscription: CustomerStripeSubscriptionResponse | None


class CustomerStripeSubscriptionResponse(BaseResponse):
    cancel_at: datetime | None
    is_active: bool
    is_trial: bool
    current_period_end_at: datetime
    product_id: str
