from uuid import UUID

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription
from tests.generator.subscription import generate


def test_create() -> None:
    result = Subscription(
        UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"),
        Email("john@doe.com"),
    )

    assert result.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert result.email == Email("john@doe.com")
    assert not result.is_active


def test_activate() -> None:
    subscription = generate()

    subscription.activate()

    assert subscription.is_active


def test_deactivate() -> None:
    subscription = generate()
    subscription.activate()

    subscription.deactivate()

    assert not subscription.is_active
