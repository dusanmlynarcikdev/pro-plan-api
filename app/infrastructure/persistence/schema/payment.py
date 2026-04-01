from datetime import date
from typing import Annotated
from uuid import UUID

from sqlalchemy import Index
from sqlmodel import Field, SQLModel

from app.domain.payment.payment import Payment
from app.domain.subscription.price import Price

from .types import Amount, Currency, Id


class PaymentSchema(SQLModel, table=True):
    __tablename__ = "payment"
    __table_args__ = (
        Index(
            "ix_payment_subscription_id_paid_at_id",
            "subscription_id",
            "paid_at",
            "id",
        ),
    )

    id: Id
    subscription_id: Annotated[
        UUID, Field(foreign_key="subscription.id", ondelete="RESTRICT")
    ]
    amount: Amount
    currency: Currency
    paid_at: date

    @classmethod
    def from_domain(cls, payment: Payment) -> PaymentSchema:
        return cls(
            id=payment.id,
            subscription_id=payment.subscription_id,
            amount=payment.price.amount,
            currency=payment.price.currency,
            paid_at=payment.paid_at,
        )

    def to_domain(self) -> Payment:
        return Payment(
            self.id,
            self.subscription_id,
            Price(self.amount, self.currency),
            self.paid_at,
        )
