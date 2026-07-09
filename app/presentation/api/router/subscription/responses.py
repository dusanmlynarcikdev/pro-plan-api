from uuid import UUID

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: UUID


class GetSubscriptionResponse(BaseModel):
    email: str
    is_active: bool
