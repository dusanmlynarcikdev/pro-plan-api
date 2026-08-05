from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID

from sqlalchemy import Column, DateTime, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.domain.customer.customer import Customer


class CustomerSchema(SQLModel, table=True):
    __tablename__ = "customers"
    __table_args__ = (
        UniqueConstraint("external_id", name="c_ui_external_id"),
        UniqueConstraint("stripe_id", name="c_ui_stripe_id"),
    )

    id: Annotated[UUID, Field(primary_key=True)]
    external_id: str
    stripe_id: str | None
    stripe_subscription_cancel_at: Annotated[
        datetime | None, Field(sa_column=Column(DateTime(timezone=True)))
    ]
    stripe_subscription_current_period_end_at: Annotated[
        datetime | None, Field(sa_column=Column(DateTime(timezone=True)))
    ]
    stripe_subscription_product_id: str | None
    stripe_subscription_status: str | None

    @classmethod
    def from_domain(cls, customer: Customer) -> CustomerSchema:
        return cls(
            id=customer.id,
            external_id=customer.external_id,
            stripe_id=customer.stripe_id,
            stripe_subscription_cancel_at=customer.stripe_subscription_cancel_at,
            stripe_subscription_current_period_end_at=customer.stripe_subscription_current_period_end_at,
            stripe_subscription_product_id=customer.stripe_subscription_product_id,
            stripe_subscription_status=customer.stripe_subscription_status,
        )

    def to_domain(self) -> Customer:
        customer = Customer(self.id, self.external_id)
        customer._stripe_id = self.stripe_id
        customer._stripe_subscription_cancel_at = self._to_utc_timezone(
            self.stripe_subscription_cancel_at
        )
        customer._stripe_subscription_current_period_end_at = self._to_utc_timezone(
            self.stripe_subscription_current_period_end_at
        )
        customer._stripe_subscription_product_id = self.stripe_subscription_product_id
        customer._stripe_subscription_status = self.stripe_subscription_status

        return customer

    def update_from_domain(self, customer: Customer) -> None:
        self.stripe_id = customer.stripe_id
        self.stripe_subscription_cancel_at = customer.stripe_subscription_cancel_at
        self.stripe_subscription_current_period_end_at = (
            customer.stripe_subscription_current_period_end_at
        )
        self.stripe_subscription_product_id = customer.stripe_subscription_product_id
        self.stripe_subscription_status = customer.stripe_subscription_status

    @staticmethod
    def _to_utc_timezone(datetime: datetime | None) -> datetime | None:
        if datetime is None:
            return None

        return datetime.astimezone(UTC)
