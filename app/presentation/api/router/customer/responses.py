from app.presentation.api.responses import BaseResponse


class CustomerResponse(BaseResponse):
    has_pro: bool
    stripe_id: str | None
