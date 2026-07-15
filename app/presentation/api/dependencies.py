from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Annotated

from fastapi.params import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from stripe import StripeClient

from app.application.stripe.billing_portal.create_session_use_case import (
    CreateSessionUseCase as CreateBillingPortalSessionUseCase_,
)
from app.application.stripe.checkout.create_session_use_case import (
    CreateSessionUseCase as CreateCheckoutSessionUseCase_,
)
from app.application.stripe.webhook.handle_event_use_case import HandleEventUseCase
from app.application.stripe.webhook.verify_use_case import VerifyUseCase
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


CreateStripeCheckoutSessionUseCase = Annotated[
    CreateCheckoutSessionUseCase_,
    Depends(get_create_checkout_session_use_case),
]


async def get_session() -> AsyncGenerator[AsyncSession]:
    async with session_factory() as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_session)]


async def get_email_sender(config: Config) -> EmailSender:
    return EmailSender(config.email_sender, config.smtp_dsn)


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


CreateStripeBillingPortalSessionUseCase = Annotated[
    CreateBillingPortalSessionUseCase_,
    Depends(get_create_billing_portal_session_use_case),
]


async def get_handle_webhook_event_use_case(
    email_sender: Annotated[EmailSender, Depends(get_email_sender)],
    session: Session,
) -> HandleEventUseCase:
    return HandleEventUseCase(email_sender, SubscriptionRepository(session))


HandleStripeWebhookEventUseCase = Annotated[
    HandleEventUseCase, Depends(get_handle_webhook_event_use_case)
]


async def get_verify_webhook_use_case(config: Config) -> VerifyUseCase:
    return VerifyUseCase(WebhookVerifier(config.stripe_webhook_secret))


VerifyStripeWebhookUseCase = Annotated[
    VerifyUseCase,
    Depends(get_verify_webhook_use_case),
]
