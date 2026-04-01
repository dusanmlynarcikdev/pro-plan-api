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
    "period, expected_date",
    ((Period.MONTHLY, date(2023, 2, 1)), (Period.YEARLY, date(2024, 1, 1))),
)
def test_renew(period: Period, expected_date: date) -> None:
    subscription = generate(period=period)

    subscription.renew(date(2023, 1, 1))

    assert subscription.expires_at == expected_date


@mark.parametrize("today", (date(2023, 1, 31), date(2023, 2, 2)))
def test_renew_outside_expires_at(today: date) -> None:
    subscription = generate()
    subscription.renew(date(2023, 1, 1))

    subscription.renew(today)

    assert subscription.expires_at == date(2023, 3, 1)
