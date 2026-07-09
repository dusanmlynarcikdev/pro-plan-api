from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import BackgroundTasks
from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.create_or_get_use_case import CreateOrGetUseCase
from app.application.subscription.get_use_case import GetUseCase
from app.infrastructure.config import Config as _Config
from app.infrastructure.config import get_config
from app.infrastructure.email_sender import EmailSender
from app.infrastructure.persistence.connection import session_factory
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)

Config = Annotated[_Config, Depends(get_config)]


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


async def get_create_or_get_subscription_use_case(
    session: Session,
) -> CreateOrGetUseCase:
    return CreateOrGetUseCase(SubscriptionRepository(session))


CreateOrGetSubscriptionUseCase = Annotated[
    CreateOrGetUseCase,
    Depends(get_create_or_get_subscription_use_case),
]


async def get_email_sender(
    background_tasks: BackgroundTasks, config: Config
) -> EmailSender:
    return EmailSender(background_tasks, config.email_sender, config.smtp_dsn)


async def get_get_subscription_use_case(
    session: Session,
) -> GetUseCase:
    return GetUseCase(SubscriptionRepository(session))


GetSubscriptionUseCase = Annotated[GetUseCase, Depends(get_get_subscription_use_case)]
