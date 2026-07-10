from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import BackgroundTasks
from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase as GetOrCreateSubscriptionUseCase_,
)
from app.application.subscription.get_subscription_use_case import (
    GetSubscriptionUseCase as GetSubscriptionUseCase_,
)
from app.infrastructure.config import Config as Config_
from app.infrastructure.config import get_config
from app.infrastructure.email_sender import EmailSender
from app.infrastructure.persistence.connection import session_factory
from app.infrastructure.persistence.repository.subscription import (
    SubscriptionRepository,
)
from app.infrastructure.stripe.client.checkout_client import (
    CheckoutClient as CheckoutClient_,
)

Config = Annotated[Config_, Depends(get_config)]


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


async def get_get_or_create_subscription_use_case(
    session: Session,
) -> GetOrCreateSubscriptionUseCase_:
    return GetOrCreateSubscriptionUseCase_(SubscriptionRepository(session))


GetOrCreateSubscriptionUseCase = Annotated[
    GetOrCreateSubscriptionUseCase_,
    Depends(get_get_or_create_subscription_use_case),
]


async def get_email_sender(
    background_tasks: BackgroundTasks, config: Config
) -> EmailSender:
    return EmailSender(background_tasks, config.email_sender, config.smtp_dsn)


async def get_get_subscription_use_case(
    session: Session,
) -> GetSubscriptionUseCase_:
    return GetSubscriptionUseCase_(SubscriptionRepository(session))


GetSubscriptionUseCase = Annotated[
    GetSubscriptionUseCase_, Depends(get_get_subscription_use_case)
]


async def get_stripe_checkout_client(config: Config) -> CheckoutClient_:
    return CheckoutClient_(config.stripe_api_key, config.stripe_checkout_success_url)


StripeCheckoutClient = Annotated[CheckoutClient_, Depends(get_stripe_checkout_client)]
