from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    is_active: bool
