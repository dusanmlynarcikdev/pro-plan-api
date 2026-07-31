from uuid import UUID

import pytest

from app.domain.customer.customer import Customer
from tests.generator.customer import generate, generate_with_subscription


def test_create() -> None:
    result = Customer(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        "user-1",
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.stripe_id is None
    assert result.stripe_product_id is None


@pytest.mark.parametrize(
    ("stripe_id", "expected_result"),
    (
        (None, False),
        ("customer-1", True),
    ),
)
def test_can_access_stripe_billing_portal(
    stripe_id: str | None, expected_result: bool
) -> None:
    customer = generate()
    customer._stripe_id = stripe_id

    assert customer.can_access_stripe_billing_portal == expected_result


def test_link_subscription() -> None:
    customer = generate()

    customer.link_subscription("customer-1", "product-1")

    assert customer.stripe_id == "customer-1"
    assert customer.stripe_product_id == "product-1"


def test_remove_subscription() -> None:
    customer = generate_with_subscription()

    customer.remove_subscription()

    assert customer.stripe_product_id is None
