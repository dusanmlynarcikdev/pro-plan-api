from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Annotated

from fastapi import BackgroundTasks
from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from stripe import StripeClient

from app.application.stripe.create_billing_portal_session_use_case import (
    CreateBillingPortalSessionUseCase as CreateBillingPortalSessionUseCase_,
)
from app.application.stripe.create_checkout_session_use_case import (
    CreateCheckoutSessionUseCase as CreateCheckoutSessionUseCase_,
)
from app.application.stripe.handle_webhook_event_use_case import (
    HandleWebhookEventUseCase as HandleWebhookEventUseCase_,
)
from app.application.stripe.verify_webhook_use_case import (
    VerifyWebhookUseCase as VerifyWebhookUseCase_,
)
from app.application.subscription.get_or_create_subscription_use_case import (
    GetOrCreateSubscriptionUseCase,
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
from app.infrastructure.stripe.billing_portal_client import BillingPortalClient
from app.infrastructure.stripe.checkout_client import CheckoutClient
from app.infrastructure.stripe.webhook_verifier import WebhookVerifier

Config = Annotated[Config_, Depends(get_config)]


async def get_create_checkout_session_use_case(
    config: Config,
    session: Session,
) -> CreateCheckoutSessionUseCase_:
    return CreateCheckoutSessionUseCase_(
        GetOrCreateSubscriptionUseCase(SubscriptionRepository(session)),
        CheckoutClient(
            get_stripe_client(config.stripe_api_key),
            config.stripe_price_id_monthly,
            config.stripe_price_id_yearly,
            str(config.stripe_checkout_success_url),
        ),
    )


CreateCheckoutSessionUseCase = Annotated[
    CreateCheckoutSessionUseCase_,
    Depends(get_create_checkout_session_use_case),
]


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


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


@lru_cache
def get_stripe_client(api_key: str) -> StripeClient:
    return StripeClient(api_key)


async def get_create_billing_portal_session_use_case(
    config: Config,
    session: Session,
) -> CreateBillingPortalSessionUseCase_:
    return CreateBillingPortalSessionUseCase_(
        BillingPortalClient(get_stripe_client(config.stripe_api_key)),
        SubscriptionRepository(session),
    )


CreateBillingPortalSessionUseCase = Annotated[
    CreateBillingPortalSessionUseCase_,
    Depends(get_create_billing_portal_session_use_case),
]


async def get_handle_webhook_event_use_case() -> HandleWebhookEventUseCase_:
    return HandleWebhookEventUseCase_()


HandleWebhookEventUseCase = Annotated[
    HandleWebhookEventUseCase_, Depends(get_handle_webhook_event_use_case)
]


async def get_verify_webhook_use_case(config: Config) -> VerifyWebhookUseCase_:
    return VerifyWebhookUseCase_(WebhookVerifier(config.stripe_webhook_secret))


VerifyWebhookUseCase = Annotated[
    VerifyWebhookUseCase_,
    Depends(get_verify_webhook_use_case),
]
