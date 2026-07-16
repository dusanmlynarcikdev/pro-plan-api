from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.domain.subscription.email import Email
from app.domain.subscription.errors import SubscriptionNotFoundError
from app.domain.subscription.subscription import Subscription
from app.infrastructure.persistence.schema.subscription import SubscriptionSchema


class SubscriptionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, subscription: Subscription) -> None:
        self._session.add(SubscriptionSchema.from_domain(subscription))
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()

    async def find_one_by_email(self, email: Email) -> Subscription | None:
        query = select(SubscriptionSchema).where(
            SubscriptionSchema.email == email.value
        )

        subscription = (await self._session.exec(query)).one_or_none()

        return subscription.to_domain() if subscription else None

    async def find_one_by_stripe_customer_id(
        self, stripe_customer_id: str
    ) -> Subscription | None:
        query = select(SubscriptionSchema).where(
            SubscriptionSchema.stripe_customer_id == stripe_customer_id
        )

        subscription = (await self._session.exec(query)).one_or_none()

        return subscription.to_domain() if subscription else None

    async def get(self, id: UUID) -> Subscription:
        """
        :raises SubscriptionNotFoundError:
        """
        subscription = await self._session.get(SubscriptionSchema, id)

        if subscription is None:
            raise SubscriptionNotFoundError

        return subscription.to_domain()

    async def get_by_email(self, email: Email) -> Subscription:
        """
        :raises SubscriptionNotFoundError:
        """
        subscription = await self.find_one_by_email(email)

        if subscription is None:
            raise SubscriptionNotFoundError()

        return subscription

    async def update(self, subscription: Subscription) -> None:
        _subscription = await self._session.get(SubscriptionSchema, subscription.id)

        if _subscription is None:
            raise RuntimeError("Subscription not found")

        _subscription.update_from_domain(subscription)
        await self._session.flush()
