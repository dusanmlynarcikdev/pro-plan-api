from uuid import UUID

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: UUID


class SubscriptionResponse(BaseModel):
    id: UUID
    email: str
    is_active: bool
