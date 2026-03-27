from sqlmodel import col, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.subscription.state import State
from app.domain.subscription.subscription import Subscription
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def find_one_open_by_email(self, email: str) -> Subscription | None:
        query = (
            select(SubscriptionSchema)
            .where(SubscriptionSchema.email == email)
            .where(col(SubscriptionSchema.state).in_((State.NEW, State.ACTIVE)))
        )

        result = await self.session.exec(query)
        subscription = result.one_or_none()

        return subscription.to_domain() if subscription else None

    async def add(self, subscription: Subscription) -> None:
        self.session.add(SubscriptionSchema.from_domain(subscription))
        await self.session.flush()

    async def update(self, subscription: Subscription) -> None:
        _subscription = await self.session.get(SubscriptionSchema, subscription.id)

        if _subscription is None:
            raise RuntimeError("Subscription not found")

        _subscription.update_from_domain(subscription)
        await self.session.flush()
