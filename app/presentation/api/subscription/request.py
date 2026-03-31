from pydantic import BaseModel

from app.domain.subscription.period import Period
from app.domain.subscription.price import Price


class CreateOrUpdateRequest(BaseModel):
    email: str
    price: Price
    period: Period
