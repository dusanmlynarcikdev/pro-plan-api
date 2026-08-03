from datetime import UTC, datetime
from typing import Annotated

from pydantic import AfterValidator

from app.presentation.api.responses import BaseResponse

type UTCDatetime = Annotated[
    datetime, AfterValidator(lambda value: value.replace(tzinfo=UTC))
]


class CustomerResponse(BaseResponse):
    stripe: CustomerStripeResponse


class CustomerStripeResponse(BaseResponse):
    can_access_billing_portal: bool
    subscription: CustomerStripeSubscriptionResponse | None


class CustomerStripeSubscriptionResponse(BaseResponse):
    cancel_at: UTCDatetime | None
    is_active: bool
    is_trial: bool
    period_end_at: UTCDatetime
    product_id: str
