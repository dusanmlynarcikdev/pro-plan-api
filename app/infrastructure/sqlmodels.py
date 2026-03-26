from datetime import date
from typing import Annotated
from uuid import UUID, uuid7

from pydantic import EmailStr
from sqlalchemy import Index, text
from sqlmodel import Field, SQLModel

from app.domain.price.price import Price
from app.domain.subscription.period import Period
from app.domain.subscription.state import State


class Subscription(SQLModel, table=True):
    __table_args__ = (
        Index(
            "uq_subscription_email_state_open",
            "_Subscription__email",
            "_Subscription__state",
            unique=True,
            postgresql_where=text("\"_Subscription__state\" IN ('new', 'active')"),
        ),
    )

    id: Annotated[UUID, Field(default_factory=uuid7, primary_key=True)]
    email: Annotated[EmailStr, Field(index=True)]
    price: Price
    period: Period
    next_payment_date: Annotated[date | None, Field(index=True)] = None
    state: Annotated[State, Field(index=True)] = State.NEW
