from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
)
from app.domain.subscription.email import Email
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema
from tests.generator.subscription import generate


async def test_create(session: AsyncSession) -> None:
    use_case = GetOrCreateSubscriptionUseCase(SubscriptionRepository(session))

    subscription = await use_case(Email("john@doe.com"))
    session.expunge_all()

    assert subscription.email.value == "john@doe.com"
    assert not subscription.is_active
    assert subscription.stripe_customer_id is None

    repository_subscription = (await session.exec(select(SubscriptionSchema))).one()

    assert repository_subscription.id == subscription.id
    assert repository_subscription.email == "john@doe.com"
    assert not repository_subscription.is_active
    assert repository_subscription.stripe_customer_id is None


async def test_create_when_another_subscription_exists(
    session: AsyncSession,
) -> None:
    session.add(SubscriptionSchema.from_domain(generate()))
    await session.flush()
    session.expunge_all()

    use_case = GetOrCreateSubscriptionUseCase(SubscriptionRepository(session))

    subscription = await use_case(Email("john2@doe.com"))
    session.expunge_all()

    assert subscription.id != UUID("019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04")

    repository_subscriptions = (await session.exec(select(SubscriptionSchema))).all()

    assert len(repository_subscriptions) == 2
    assert repository_subscriptions[0].id == UUID(
        "019d2a4c-ab5d-7a0c-87bb-d4306b6d9d04"
    )
    assert repository_subscriptions[1].id == subscription.id
