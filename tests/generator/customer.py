from datetime import UTC, datetime
from uuid import UUID

from app.domain.customer.customer import Customer

_DEFAULT_ID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


def generate(
    id: UUID = _DEFAULT_ID,
    external_id: str = "user-1",
) -> Customer:
    return Customer(id, external_id)


def generate_with_stripe() -> Customer:
    customer = generate()
    customer.set_stripe(
        "customer-1",
        "product-1",
        "trialing",
        datetime(2026, 1, 1, 12, 30, 45, tzinfo=UTC),
        datetime(2027, 2, 2, 13, 35, 50, tzinfo=UTC),
    )

    return customer
