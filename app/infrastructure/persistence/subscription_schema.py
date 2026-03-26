from datetime import date
from decimal import Decimal
from typing import Annotated
from uuid import UUID

from sqlalchemy import Index, text
from sqlmodel import Field, SQLModel

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State
from app.domain.subscription.subscription import Subscription


class SubscriptionSchema(SQLModel, table=True):
    __tablename__ = "subscription"

    __table_args__ = (
        Index(
            "uq_subscription_email",
            "email",
            unique=True,
            postgresql_where=text("state IN ('new', 'active')"),
        ),
    )

    id: Annotated[UUID, Field(primary_key=True)]
    email: Annotated[str, Field(index=True)]
    amount: Annotated[Decimal, Field(max_digits=12, decimal_places=2)]
    currency: Annotated[str, Field(min_length=3, max_length=3)]
    period: Period
    next_payment_date: Annotated[date | None, Field(index=True)]
    state: Annotated[State, Field(index=True)]

    @classmethod
    def from_domain(cls, subscription: Subscription) -> "SubscriptionSchema":
        return cls(
            id=subscription.id,
            email=subscription.email.value,
            amount=subscription.price.amount,
            currency=subscription.price.currency,
            period=subscription.period,
            next_payment_date=subscription.next_payment_date,
            state=subscription.state,
        )

    def to_domain(self) -> Subscription:
        subscription = Subscription(
            self.id,
            Email(self.email),
            Price(self.amount, self.currency),
            self.period,
        )
        setattr(
            subscription, "_Subscription__next_payment_date", self.next_payment_date
        )
        setattr(subscription, "_Subscription__state", self.state)

        return subscription
