from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    can_access_stripe_billing_portal: bool
    has_active_subscription: bool
    stripe_product_id: str | None
