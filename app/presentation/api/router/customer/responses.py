from pydantic import BaseModel


class CustomerResponse(BaseModel):
    has_pro: bool
    stripe_id: str | None
