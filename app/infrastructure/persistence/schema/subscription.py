from datetime import date
from typing import Annotated
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.subscription import Subscription


class SubscriptionSchema(SQLModel, table=True):
    __tablename__ = "subscription"
    __table_args__ = (UniqueConstraint("email", name="uq_subscription_email"),)

    id: Annotated[UUID, Field(primary_key=True)]
    email: str
    period: Period
    expires_at: date | None

    @classmethod
    def from_domain(cls, subscription: Subscription) -> SubscriptionSchema:
        return cls(
            id=subscription.id,
            email=subscription.email.value,
            period=subscription.period,
            expires_at=subscription.expires_at,
        )

    def to_domain(self) -> Subscription:
        subscription = Subscription(
            self.id,
            Email(self.email),
            self.period,
        )
        setattr(subscription, "_Subscription__expires_at", self.expires_at)

        return subscription

    def update_from_domain(self, subscription: Subscription) -> None:
        self.period = subscription.period
        self.expires_at = subscription.expires_at
