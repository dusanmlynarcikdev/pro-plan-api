from uuid import UUID

from app.infrastructure.database.schema.customer import CustomerSchema
from tests.generator.customer import generate, generate_with_stripe


def test_from_domain() -> None:
    result = CustomerSchema.from_domain(generate_with_stripe())

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.stripe_id == "customer-1"
    assert result.stripe_subscription_product_id == "product-1"
    assert result.stripe_subscription_status == "trialing"


def test_to_domain() -> None:
    schema = CustomerSchema(
        id=UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        external_id="user-1",
        stripe_id="customer-1",
        stripe_subscription_product_id="product-1",
        stripe_subscription_status="trialing",
    )

    result = schema.to_domain()

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.stripe_id == "customer-1"
    assert result.stripe_subscription_product_id == "product-1"
    assert result.stripe_subscription_status == "trialing"


def test_update_from_domain() -> None:
    schema = CustomerSchema.from_domain(generate())

    schema.update_from_domain(generate_with_stripe())

    assert schema.stripe_id == "customer-1"
    assert schema.stripe_subscription_product_id == "product-1"
    assert schema.stripe_subscription_status == "trialing"
