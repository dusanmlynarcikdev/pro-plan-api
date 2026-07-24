from uuid import UUID

from app.domain.customer.customer import Customer

_DEFAULT_ID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")


def generate(
    id: UUID = _DEFAULT_ID,
    external_id: str = "user-1",
) -> Customer:
    return Customer(id, external_id)
