from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    has_active_subscription: bool
    stripe: Stripe


class Stripe(BaseResponse):
    can_access_billing_portal: bool
    subscription_product_id: str | None
