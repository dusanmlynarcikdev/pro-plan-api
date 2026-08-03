from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.domain.customer.customer import Customer
from tests.generator.customer import generate


def test_create() -> None:
    result = Customer(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        "user-1",
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.external_id == "user-1"
    assert result.stripe_id is None
    assert result.stripe_subscription_cancel_at is None
    assert result.stripe_subscription_period_end_at is None
    assert result.stripe_subscription_product_id is None
    assert result.stripe_subscription_status is None


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

    assert customer.can_access_stripe_billing_portal() == expected_result


@pytest.mark.parametrize(
    ("stripe_subscription_status", "expected_result"),
    (
        (None, False),
        ("active", True),
        ("trialing", True),
        ("past_due", True),
        ("canceled", False),
    ),
)
def test_is_stripe_subscription_active(
    stripe_subscription_status: str | None, expected_result: bool
) -> None:
    customer = generate()
    customer._stripe_subscription_status = stripe_subscription_status

    assert customer.is_stripe_subscription_active() == expected_result


@pytest.mark.parametrize(
    ("stripe_subscription_status", "expected_result"),
    (
        (None, False),
        ("trialing", True),
        ("canceled", False),
    ),
)
def test_is_stripe_subscription_trial(
    stripe_subscription_status: str | None, expected_result: bool
) -> None:
    customer = generate()
    customer._stripe_subscription_status = stripe_subscription_status

    assert customer.is_stripe_subscription_trial() == expected_result


def test_set_stripe() -> None:
    customer = generate()

    customer.set_stripe(
        "customer-1",
        datetime(2027, 2, 2, 13, 35, 50, tzinfo=UTC),
        datetime(2026, 1, 1, 12, 30, 45, tzinfo=UTC),
        "product-1",
        "active",
    )

    assert customer.stripe_id == "customer-1"
    assert customer.stripe_subscription_cancel_at == datetime(
        2027, 2, 2, 13, 35, 50, tzinfo=UTC
    )
    assert customer.stripe_subscription_period_end_at == datetime(
        2026, 1, 1, 12, 30, 45, tzinfo=UTC
    )
    assert customer.stripe_subscription_product_id == "product-1"
    assert customer.stripe_subscription_status == "active"
