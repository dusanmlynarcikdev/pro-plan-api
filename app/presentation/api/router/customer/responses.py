from datetime import datetime

from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    stripe: CustomerStripeResponse


class CustomerStripeResponse(BaseResponse):
    can_access_billing_portal: bool
    subscription: CustomerStripeSubscriptionResponse | None


class CustomerStripeSubscriptionResponse(BaseResponse):
    is_active: bool
    is_cancelling: bool
    is_trial: bool
    period_end_at: datetime
    product_id: str
