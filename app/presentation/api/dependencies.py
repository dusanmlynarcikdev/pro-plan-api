from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.create_or_update_command import (
    CreateOrUpdateSubscriptionCommand as _CreateOrUpdateSubscriptionCommand,
)
from app.infrastructure.persistence.connection import session_factory
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session
        await session.commit()


Session = Annotated[AsyncSession, Depends(get_session)]


async def get_create_or_update_subscription_command(
    session: Session,
) -> _CreateOrUpdateSubscriptionCommand:
    return _CreateOrUpdateSubscriptionCommand(SubscriptionRepository(session))


CreateOrUpdateSubscriptionCommand = Annotated[
    _CreateOrUpdateSubscriptionCommand,
    Depends(get_create_or_update_subscription_command),
]
