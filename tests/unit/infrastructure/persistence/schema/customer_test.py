from uuid import UUID

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate, generate_with_subscription


def test_from_domain() -> None:
    result = CustomerSchema.from_domain(generate_with_subscription())

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.has_active_subscription
    assert result.stripe_id == "customer-1"
    assert result.stripe_product_id == "product-1"


def test_to_domain() -> None:
    schema = CustomerSchema(
        id=UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        external_id="user-1",
        has_active_subscription=True,
        stripe_id="customer-1",
        stripe_product_id="product-1",
    )

    result = schema.to_domain()

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.has_active_subscription
    assert result.stripe_id == "customer-1"
    assert result.stripe_product_id == "product-1"


def test_update_from_domain() -> None:
    schema = CustomerSchema.from_domain(generate())

    schema.update_from_domain(generate_with_subscription())

    assert schema.has_active_subscription
    assert schema.stripe_id == "customer-1"
    assert schema.stripe_product_id == "product-1"
