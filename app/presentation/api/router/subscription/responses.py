from pydantic import BaseModel


class SubscriptionResponse(BaseModel):
    is_active: bool
    stripe_customer_id: str | None
