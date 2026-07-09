from pydantic import BaseModel


class GetSubscriptionResponse(BaseModel):
    email: str
    is_active: bool
