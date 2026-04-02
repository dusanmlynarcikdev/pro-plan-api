from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.create_or_update_use_case import (
    CreateOrUpdateSubscriptionUseCase as _CreateOrUpdateSubscriptionUseCase,
)
from app.application.subscription.get_use_case import (
    GetSubscriptionUseCase as _GetSubscriptionUseCase,
)
from app.application.subscription.renewal_use_case import (
    RenewalSubscriptionUseCase as _RenewalSubscriptionUseCase,
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


async def get_create_or_update_subscription_use_case(
    session: Session,
) -> _CreateOrUpdateSubscriptionUseCase:
    return _CreateOrUpdateSubscriptionUseCase(SubscriptionRepository(session))


CreateOrUpdateSubscriptionUseCase = Annotated[
    _CreateOrUpdateSubscriptionUseCase,
    Depends(get_create_or_update_subscription_use_case),
]


async def get_renewal_subscription_use_case(
    session: Session,
) -> _RenewalSubscriptionUseCase:
    return _RenewalSubscriptionUseCase(SubscriptionRepository(session))


RenewalSubscriptionUseCase = Annotated[
    _RenewalSubscriptionUseCase, Depends(get_renewal_subscription_use_case)
]


async def get_get_subscription_use_case(
    session: Session,
) -> _GetSubscriptionUseCase:
    return _GetSubscriptionUseCase(SubscriptionRepository(session))


GetSubscriptionUseCase = Annotated[
    _GetSubscriptionUseCase, Depends(get_get_subscription_use_case)
]
