from fastapi import APIRouter, HTTPException, status

from app.domain.subscription.email import Email
from app.infrastructure.config import get_config
from app.infrastructure.stripe.client.errors import ClientError
from app.infrastructure.stripe.router.dependencies import StripeClient
from app.infrastructure.stripe.router.requests import (
    BillingPeriod,
    CreateCheckoutSessionRequest,
)
from app.infrastructure.stripe.router.responses import UrlResponse
from app.presentation.api.dependencies import CreateOrGetSubscriptionUseCase

CONFIG = get_config()
PRICE_IDS = {
    BillingPeriod.MONTHLY: CONFIG.stripe_price_id_monthly,
    BillingPeriod.YEARLY: CONFIG.stripe_price_id_yearly,
}

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    client: StripeClient,
    create_or_get_subscription: CreateOrGetSubscriptionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    subscription = await create_or_get_subscription(Email(request.email))

    try:
        redirect_url = await client.create_checkout_session(
            PRICE_IDS[request.billing_period], subscription.id
        )
    except ClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Stripe checkout session",
        )

    return UrlResponse(url=redirect_url)
