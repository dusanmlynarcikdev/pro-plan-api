from uuid import UUID

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate, generate_with_subscription


def test_from_domain() -> None:
    customer = generate_with_subscription()

    result = CustomerSchema.from_domain(customer)

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.has_pro
    assert result.stripe_id == "cus-1"
    assert result.stripe_product_id == "prod-1"


def test_to_domain() -> None:
    schema = CustomerSchema(
        id=UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        external_id="user-1",
        has_pro=True,
        stripe_id="cus-1",
        stripe_product_id="prod-1",
    )

    result = schema.to_domain()

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.has_pro
    assert result.stripe_id == "cus-1"
    assert result.stripe_product_id == "prod-1"


def test_update_from_domain() -> None:
    customer = generate_with_subscription()
    schema = CustomerSchema.from_domain(generate())

    schema.update_from_domain(customer)

    assert schema.has_pro
    assert schema.stripe_id == "cus-1"
    assert schema.stripe_product_id == "prod-1"
