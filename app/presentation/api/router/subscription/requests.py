from pydantic import BaseModel

from app.domain.subscription.period import Period


class CreateOrUpdateRequest(BaseModel):
    email: str
    period: Period
