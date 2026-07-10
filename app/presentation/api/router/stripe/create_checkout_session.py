from fastapi import APIRouter, HTTPException, status

from app.domain.subscription.email import Email
from app.infrastructure.stripe.client.errors import ClientError
from app.presentation.api.dependencies import (
    Config,
    CreateOrGetSubscriptionUseCase,
    StripeClient,
)
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    client: StripeClient,
    config: Config,
    create_or_get_subscription: CreateOrGetSubscriptionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    subscription = await create_or_get_subscription(Email(request.email))

    try:
        redirect_url = await client.create_checkout_session(
            request.billing_period.get_stripe_price_id(config), subscription.id
        )
    except ClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Stripe checkout session",
        )

    return UrlResponse(url=redirect_url)
