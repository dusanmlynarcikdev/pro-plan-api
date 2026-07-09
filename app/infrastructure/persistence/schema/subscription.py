from typing import Annotated
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription


class SubscriptionSchema(SQLModel, table=True):
    __tablename__ = "subscription"
    __table_args__ = (UniqueConstraint("email", name="uq_subscription_email"),)

    id: Annotated[UUID, Field(primary_key=True)]
    email: str
    is_active: bool

    @classmethod
    def from_domain(cls, subscription: Subscription) -> SubscriptionSchema:
        return cls(
            id=subscription.id,
            email=subscription.email.value,
            is_active=subscription.is_active,
        )

    def to_domain(self) -> Subscription:
        return Subscription(self.id, Email(self.email))

    def update_from_domain(self, subscription: Subscription) -> None:
        self.is_active = subscription.is_active
