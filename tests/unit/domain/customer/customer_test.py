from uuid import UUID

import pytest

from app.domain.customer.customer import Customer
from app.domain.customer.email import Email
from tests.generator.customer import generate


def test_create() -> None:
    result = Customer(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        Email("john@doe.com"),
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == Email("john@doe.com")
    assert not result.has_pro
    assert result.stripe_id is None


def test_link_stripe_subscription() -> None:
    customer = generate()

    customer.link_stripe_subscription("cus_123")

    assert customer.has_pro
    assert customer.stripe_id == "cus_123"


@pytest.mark.parametrize(
    ("has_pro", "stripe_id", "expected_result"),
    (
        (False, None, False),
        (False, "cus_123", False),
        (True, None, False),
        (True, "cus_123", True),
    ),
)
def test_has_stripe_subscription(
    has_pro: bool, stripe_id: str | None, expected_result: bool
) -> None:
    customer = generate()
    customer._has_pro = has_pro
    customer._stripe_id = stripe_id

    assert customer.has_stripe_subscription() == expected_result


def test_deactivate_pro() -> None:
    customer = generate()
    customer._has_pro = True

    customer.deactivate_pro()

    assert not customer.has_pro
