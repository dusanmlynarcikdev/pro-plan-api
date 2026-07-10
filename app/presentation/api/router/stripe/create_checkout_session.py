from fastapi import APIRouter, HTTPException, status

from app.domain.subscription.email import Email
from app.infrastructure.stripe.client.errors import CheckoutError
from app.presentation.api.dependencies import (
    Config,
    GetOrCreateSubscriptionUseCase,
    StripeCheckoutClient,
)
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    client: StripeCheckoutClient,
    config: Config,
    get_or_create_subscription: GetOrCreateSubscriptionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    subscription = await get_or_create_subscription(Email(request.email))

    try:
        checkout_url = await client.create_session(
            request.billing_period.get_stripe_price_id(config), subscription.id
        )
    except CheckoutError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Stripe checkout session",
        )

    return UrlResponse(url=checkout_url)
