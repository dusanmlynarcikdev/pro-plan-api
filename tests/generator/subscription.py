from uuid import UUID

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription


def generate(
    id: UUID = UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
    email: Email = Email("john@doe.com"),
    stripe_customer_id: str | None = None,
) -> Subscription:
    subscription = Subscription(id, email)

    if stripe_customer_id is not None:
        subscription._stripe_customer_id = stripe_customer_id

    return subscription
