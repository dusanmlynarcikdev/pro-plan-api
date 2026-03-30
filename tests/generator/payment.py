from datetime import date
from decimal import Decimal
from uuid import UUID

from app.domain.payment.payment import Payment
from app.domain.subscription.price import Price


def generate(
    id: UUID = UUID("019d3e91-911c-7f71-80ce-276ef0cff36e"),
    price: Price = Price(Decimal("1"), "USD"),
    paid_at: date = date(2026, 1, 1),
) -> Payment:
    return Payment(
        id,
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        price,
        paid_at,
    )
