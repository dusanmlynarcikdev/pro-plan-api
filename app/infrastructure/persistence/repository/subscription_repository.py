from sqlalchemy.orm.util import identity_key
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
        key = identity_key(SubscriptionSchema, (subscription.id,))
        stored = self.session.sync_session.identity_map.get(key)

        if stored is None:
            raise RuntimeError(
                f"Subscription {subscription.id} is not loaded in the current session"
            )

        stored.update_from_domain(subscription)
        await self.session.flush()
