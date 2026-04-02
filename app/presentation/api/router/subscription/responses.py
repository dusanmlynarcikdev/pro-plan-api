from datetime import date

from pydantic import BaseModel

from app.domain.subscription.period import Period


class GetSubscriptionResponse(BaseModel):
    email: str
    period: Period
    expires_at: date | None
    is_active: bool
