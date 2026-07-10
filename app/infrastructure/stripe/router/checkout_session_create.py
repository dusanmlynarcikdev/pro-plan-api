from fastapi import APIRouter

from app.domain.subscription.email import Email
from app.infrastructure.config import get_config
from app.infrastructure.stripe.router.dependencies import StripeClient
from app.infrastructure.stripe.router.requests import (
    CreateCheckoutSessionRequest,
    SubscriptionPeriod,
)
from app.infrastructure.stripe.router.responses import UrlResponse
from app.presentation.api.dependencies import CreateOrGetSubscriptionUseCase

CONFIG = get_config()
PRICE_IDS = {
    SubscriptionPeriod.MONTHLY: CONFIG.stripe_price_id_monthly,
    SubscriptionPeriod.YEARLY: CONFIG.stripe_price_id_yearly,
}

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    client: StripeClient,
    create_or_get_subscription: CreateOrGetSubscriptionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    subscription = await create_or_get_subscription(Email(request.email))
    redirect_url = await client.create_checkout_session(
        PRICE_IDS[request.period], subscription.id
    )

    return UrlResponse(url=redirect_url)
