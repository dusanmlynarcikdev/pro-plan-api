from uuid import UUID

from app.domain.customer.customer import Customer
from app.domain.customer.email import Email


def generate(
    id: UUID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    email: Email = Email("john@doe.com"),
) -> Customer:
    return Customer(id, email)
