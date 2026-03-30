from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.create_update import CreateUpdateSubscription
from app.infrastructure.persistence.connection import session_factory
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session
        await session.commit()


Session = Annotated[AsyncSession, Depends(get_session)]


async def get_create_update_subscription_command(
    session: Session,
) -> CreateUpdateSubscription:
    return CreateUpdateSubscription(SubscriptionRepository(session))


CreateUpdateSubscriptionDependency = Annotated[
    CreateUpdateSubscription, Depends(get_create_update_subscription_command)
]
