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
        ("cus_123", True),
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

    customer.link_subscription("cus-1", "prod-1")

    assert customer.stripe_id == "cus-1"
    assert customer.stripe_product_id == "prod-1"


@pytest.mark.parametrize(
    ("stripe_id", "stripe_product_id", "expected_result"),
    (
        (None, None, False),
        (None, "product-1", False),
        ("customer-1", None, False),
        ("customer-1", "product-1", True),
    ),
)
def test_has_subscription(
    stripe_id: str | None, stripe_product_id: str | None, expected_result: bool
) -> None:
    customer = generate()
    customer._stripe_id = stripe_id
    customer._stripe_product_id = stripe_product_id

    assert customer.has_subscription() == expected_result


def test_remove_subscription() -> None:
    customer = generate_with_subscription()

    customer.remove_subscription()

    assert customer.stripe_product_id is None
