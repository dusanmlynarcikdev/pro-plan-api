from datetime import date
from uuid import UUID

from pytest import mark

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.subscription import Subscription
from tests.generator.subscription import generate


def test_create() -> None:
    result = Subscription(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        Email("john@doe.com"),
        Period.MONTHLY,
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == Email("john@doe.com")
    assert result.period == Period.MONTHLY
    assert result.expires_at is None


@mark.parametrize(
    "period, today, expected_date",
    (
        (Period.MONTHLY, date(2026, 1, 1), date(2026, 2, 1)),
        (Period.MONTHLY, date(2026, 1, 31), date(2026, 2, 28)),
        (Period.MONTHLY, date(2024, 1, 31), date(2024, 2, 29)),
        (Period.MONTHLY, date(2026, 2, 28), date(2026, 3, 31)),
        (Period.YEARLY, date(2026, 1, 1), date(2027, 1, 1)),
        (Period.YEARLY, date(2023, 2, 28), date(2024, 2, 29)),
        (Period.YEARLY, date(2024, 2, 29), date(2025, 2, 28)),
    ),
)
def test_renew(period: Period, today: date, expected_date: date) -> None:
    subscription = generate(period=period)

    subscription.renew(today)

    assert subscription.expires_at == expected_date


def test_renew_before_expiration() -> None:
    subscription = generate()
    setattr(subscription, "_Subscription__expires_at", date(2026, 1, 1))

    subscription.renew(date(2025, 12, 31))

    assert subscription.expires_at == date(2026, 2, 1)


@mark.parametrize(
    "expires_at, expected_result",
    (
        (date(2026, 1, 1), True),
        (date(2026, 1, 2), True),
        (date(2025, 12, 31), False),
    ),
)
def test_is_active(expires_at: date, expected_result: bool) -> None:
    subscription = generate()
    setattr(subscription, "_Subscription__expires_at", expires_at)

    assert subscription.is_active(date(2026, 1, 1)) == expected_result


def test_is_active_expires_at_is_none() -> None:
    subscription = generate()

    assert subscription.is_active(date(2026, 1, 1)) == False
