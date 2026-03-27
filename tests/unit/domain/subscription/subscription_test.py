from datetime import date
from decimal import Decimal
from uuid import UUID

from pytest import mark, raises

from app.domain.subscription.email import Email
from app.domain.subscription.errors import SubscriptionCanceled, SubscriptionExpired
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State
from app.domain.subscription.subscription import Subscription
from tests.generator.subscription import generate


def test_create() -> None:
    result = Subscription(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        Email("john@doe.com"),
        Price(Decimal("1"), "USD"),
        Period.MONTHLY,
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == Email("john@doe.com")
    assert result.price == Price(Decimal("1"), "USD")
    assert result.period == Period.MONTHLY
    assert result.next_payment_date is None
    assert result.state == State.NEW


def test_change() -> None:
    subscription = generate()

    subscription.change(Price(Decimal("2"), "CZK"), Period.YEARLY)

    assert subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert subscription.email == Email("john@doe.com")
    assert subscription.price == Price(Decimal("2"), "CZK")
    assert subscription.period == Period.YEARLY
    assert subscription.next_payment_date is None
    assert subscription.state == State.NEW


@mark.parametrize(
    "period, expected_date",
    ((Period.MONTHLY, date(2023, 2, 1)), (Period.YEARLY, date(2024, 1, 1))),
)
def test_renew(period: Period, expected_date: date) -> None:
    subscription = generate(period=period)

    subscription.renew(payment_date=date(2023, 1, 1))

    assert subscription.next_payment_date == expected_date
    assert subscription.state == State.ACTIVE


@mark.parametrize("payment_date", (date(2023, 1, 31), date(2023, 2, 2)))
def test_renew_outside_next_payment_date(payment_date: date) -> None:
    subscription = generate()
    subscription.renew(date(2023, 1, 1))

    subscription.renew(payment_date)

    assert subscription.next_payment_date == date(2023, 3, 1)
    assert subscription.state == State.ACTIVE


def test_cancel() -> None:
    subscription = generate()

    subscription.cancel()

    assert subscription.next_payment_date is None
    assert subscription.state == State.CANCELED


def test_canceled_expired() -> None:
    subscription = generate()
    subscription.cancel()

    with raises(SubscriptionCanceled):
        subscription.cancel()


def test_cancel_expired() -> None:
    subscription = generate()
    subscription.expire()

    with raises(SubscriptionExpired):
        subscription.cancel()


def test_expire() -> None:
    subscription = generate()
    subscription.renew(date(2023, 1, 1))

    subscription.expire()

    assert subscription.next_payment_date is None
    assert subscription.state == State.EXPIRED


def test_expire_canceled() -> None:
    subscription = generate()
    subscription.cancel()

    with raises(SubscriptionCanceled):
        subscription.expire()


def test_expire_expired() -> None:
    subscription = generate()
    subscription.expire()

    with raises(SubscriptionExpired):
        subscription.expire()
