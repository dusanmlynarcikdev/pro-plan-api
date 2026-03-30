from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, subscription: Subscription) -> None:
        self.session.add(SubscriptionSchema.from_domain(subscription))
        await self.session.flush()

    async def find_one_by_email(self, email: Email) -> Subscription | None:
        query = select(SubscriptionSchema).where(
            SubscriptionSchema.email == email.value
        )

        result = await self.session.exec(query)
        subscription = result.one_or_none()

        return subscription.to_domain() if subscription else None

    async def update(self, subscription: Subscription) -> None:
        _subscription = await self.session.get(SubscriptionSchema, subscription.id)

        if _subscription is None:
            raise RuntimeError("Subscription not found")

        _subscription.update_from_domain(subscription)
        await self.session.flush()
