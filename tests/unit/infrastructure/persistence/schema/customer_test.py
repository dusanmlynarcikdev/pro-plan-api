from uuid import UUID

from app.domain.customer.email import Email
from app.infrastructure.persistence.schema.customer import CustomerSchema
from tests.generator.customer import generate


def test_from_domain() -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")

    result = CustomerSchema.from_domain(customer)

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == "john@doe.com"
    assert result.has_pro
    assert result.stripe_id == "cus_123"


def test_to_domain() -> None:
    schema = CustomerSchema(
        id=UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        email="john@doe.com",
        has_pro=True,
        stripe_id="cus_123",
    )

    result = schema.to_domain()

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == Email("john@doe.com")
    assert result.has_pro
    assert result.stripe_id == "cus_123"


def test_update_from_domain() -> None:
    customer = generate()
    customer.link_stripe_subscription("cus_123")
    schema = CustomerSchema.from_domain(generate())

    schema.update_from_domain(customer)

    assert schema.has_pro
    assert schema.stripe_id == "cus_123"
