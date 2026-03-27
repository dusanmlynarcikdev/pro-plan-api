from decimal import Decimal

from pytest import mark, raises

from app.domain.subscription.errors import InvalidAmount, InvalidCurrency
from app.domain.subscription.price import Price


def test_create() -> None:
    result = Price(Decimal("1.5"), "USD")

    assert result.amount == Decimal("1.5")
    assert result.currency == "USD"


@mark.parametrize("price", ("0", "0.0", "-1.5"))
def test_invalid_amount(price: str) -> None:
    with raises(InvalidAmount):
        Price(Decimal(price), "USD")


@mark.parametrize("currency", ("", "XYZ"))
def test_invalid_currency(currency: str) -> None:
    with raises(InvalidCurrency):
        Price(Decimal("1"), currency)
