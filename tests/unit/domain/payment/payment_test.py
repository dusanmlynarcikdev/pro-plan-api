from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.payment.payment import Payment
from tests.generator.subscription import generate


def test_from_subscription() -> None:
    result = Payment.from_subscription(generate(), date(2026, 1, 1))

    assert result.subscription_id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.price.amount == Decimal("1")
    assert result.price.currency == "USD"
    assert result.paid_at == date(2026, 1, 1)
