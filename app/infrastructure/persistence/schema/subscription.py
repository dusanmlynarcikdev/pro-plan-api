from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State
from app.domain.subscription.subscription import Subscription


class SubscriptionSchema(SQLModel, table=True):
    __tablename__ = "subscription"
    __table_args__ = (UniqueConstraint("email", name="uq_subscription_email"),)

    id: Annotated[UUID, Field(primary_key=True)]
    email: str
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    currency: Annotated[str, Field(min_length=3, max_length=3)]
    period: Period
    expires_at: Annotated[date | None, Field(index=True)]
    state: Annotated[State, Field(index=True)]

    @classmethod
    def from_domain(cls, subscription: Subscription) -> SubscriptionSchema:
        return cls(
            id=subscription.id,
            email=subscription.email.value,
            amount=subscription.price.amount,
            currency=subscription.price.currency,
            period=subscription.period,
            expires_at=subscription.expires_at,
            state=subscription.state,
        )

    def to_domain(self) -> Subscription:
        subscription = Subscription(
            self.id,
            Email(self.email),
            Price(self.amount, self.currency),
            self.period,
        )
        setattr(subscription, "_Subscription__expires_at", self.expires_at)
        setattr(subscription, "_Subscription__state", self.state)

        return subscription

    def update_from_domain(self, subscription: Subscription) -> None:
        self.amount = subscription.price.amount
        self.currency = subscription.price.currency
        self.period = subscription.period
        self.expires_at = subscription.expires_at
        self.state = subscription.state
