from typing import Annotated
from uuid import UUID

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.domain.customer.customer import Customer
from app.domain.customer.email import Email


class CustomerSchema(SQLModel, table=True):
    __tablename__ = "customer"
    __table_args__ = (
        UniqueConstraint("email", name="c_ui_email"),
        UniqueConstraint("stripe_id", name="c_ui_stripe_id"),
    )

    id: Annotated[UUID, Field(primary_key=True)]
    email: str
    has_pro: bool
    stripe_id: str | None

    @classmethod
    def from_domain(cls, customer: Customer) -> CustomerSchema:
        return cls(
            id=customer.id,
            email=customer.email.value,
            has_pro=customer.has_pro,
            stripe_id=customer.stripe_id,
        )

    def to_domain(self) -> Customer:
        customer = Customer(self.id, Email(self.email))
        customer._has_pro = self.has_pro
        customer.stripe_id = self.stripe_id

        return customer

    def update_from_domain(self, customer: Customer) -> None:
        self.has_pro = customer.has_pro
        self.stripe_id = customer.stripe_id
