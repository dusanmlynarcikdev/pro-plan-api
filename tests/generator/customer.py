from uuid import UUID

from app.domain.customer.customer import Customer


def generate(
    id: UUID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    external_id: str = "user-1",
) -> Customer:
    return Customer(id, external_id)
