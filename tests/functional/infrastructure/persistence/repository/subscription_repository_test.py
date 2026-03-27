from datetime import date
from decimal import Decimal
from uuid import UUID

from pytest import raises
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.subscription.period import Period
from app.domain.subscription.price import Price
from app.domain.subscription.state import State
from app.infrastructure.persistence.repository.subscription_repository import (
    SubscriptionRepository,
)
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate


async def test_add(session: AsyncSession) -> None:
    subscription = generate()
    subscription.renewal(date(2026, 1, 1))

    await SubscriptionRepository(session).add(subscription)
    session.expunge_all()

    repository_subscription = await get_subscription(session, subscription.id)

    assert repository_subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_subscription.email == "john@doe.com"
    assert repository_subscription.amount == Decimal("1")
    assert repository_subscription.currency == "USD"
    assert repository_subscription.period == Period.MONTHLY
    assert repository_subscription.next_payment_date == date(2026, 2, 1)
    assert repository_subscription.state == State.ACTIVE


async def test_update(session: AsyncSession) -> None:
    subscription = generate()
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()
    session.expunge_all()

    subscription.change(Price(Decimal("2"), "CZK"), Period.YEARLY)
    subscription.renewal(date(2026, 2, 1))

    await SubscriptionRepository(session).update(subscription)
    session.expunge_all()

    repository_subscription = await get_subscription(session, subscription.id)

    assert repository_subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_subscription.email == "john@doe.com"
    assert repository_subscription.amount == Decimal("2")
    assert repository_subscription.currency == "CZK"
    assert repository_subscription.period == Period.YEARLY
    assert repository_subscription.next_payment_date == date(2027, 2, 1)
    assert repository_subscription.state == State.ACTIVE


async def test_update_unknown_subscription(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    with raises(RuntimeError, match="Subscription not found"):
        await SubscriptionRepository(session).update(
            generate(UUID("019d2fb0-b4d2-7731-9924-9de4130ec63e"))
        )


async def test_find_one_open_by_email_new_exists(session: AsyncSession) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_subscription = await SubscriptionRepository(
        session
    ).find_one_open_by_email("john@doe.com")

    assert repository_subscription is not None
    assert repository_subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_subscription.email.value == "john@doe.com"
    assert repository_subscription.price.amount == Decimal("1")
    assert repository_subscription.price.currency == "USD"
    assert repository_subscription.period == Period.MONTHLY
    assert repository_subscription.next_payment_date is None
    assert repository_subscription.state == State.NEW


async def test_find_one_open_by_email_active_exists(session: AsyncSession) -> None:
    subscription = generate()
    subscription.renewal(date(2026, 1, 1))
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()
    session.expunge_all()

    repository_subscription = await SubscriptionRepository(
        session
    ).find_one_open_by_email("john@doe.com")

    assert repository_subscription is not None
    assert repository_subscription.id == UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")
    assert repository_subscription.email.value == "john@doe.com"
    assert repository_subscription.price.amount == Decimal("1")
    assert repository_subscription.price.currency == "USD"
    assert repository_subscription.period == Period.MONTHLY
    assert repository_subscription.next_payment_date == date(2026, 2, 1)
    assert repository_subscription.state == State.ACTIVE


async def test_find_one_open_by_email_expired_exists(session: AsyncSession) -> None:
    subscription = generate()
    subscription.expire()
    session.add(SubscriptionSchema.from_domain(subscription))
    await session.flush()
    session.expunge_all()

    repository_subscription = await SubscriptionRepository(
        session
    ).find_one_open_by_email("john@doe.com")

    assert repository_subscription is None


async def test_find_one_open_by_email_another_subscription_exists(
    session: AsyncSession,
) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    repository_subscription = await SubscriptionRepository(
        session
    ).find_one_open_by_email("john2@doe.com")

    assert repository_subscription is None


async def test_find_one_open_by_email_empty_repository(
    session: AsyncSession,
) -> None:
    repository_subscription = await SubscriptionRepository(
        session
    ).find_one_open_by_email("john@doe.com")

    assert repository_subscription is None


async def get_subscription(session: AsyncSession, id: UUID) -> SubscriptionSchema:
    query = select(SubscriptionSchema).where(SubscriptionSchema.id == id)
    result = await session.exec(query)

    return result.one()
