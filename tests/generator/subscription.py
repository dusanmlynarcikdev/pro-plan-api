from decimal import Decimal
from uuid import UUID

from app.domain.subscription.email import Email
from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.subscription import Subscription


def generate(
    id: UUID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    email: Email = Email("john@doe.com"),
    period: Period = Period.MONTHLY,
) -> Subscription:
    return Subscription(
        id,
        email,
        Price(Decimal("1"), "USD"),
        period,
    )
