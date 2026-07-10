from fastapi import APIRouter, HTTPException, status

from app.domain.subscription.email import Email
from app.infrastructure.stripe.client.errors import ClientError
from app.presentation.api.dependencies import (
    CheckoutClient,
    Config,
    CreateOrGetSubscriptionUseCase,
)
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    client: CheckoutClient,
    config: Config,
    create_or_get_subscription: CreateOrGetSubscriptionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    subscription = await create_or_get_subscription(Email(request.email))

    try:
        session_url = await client.create_session(
            request.billing_period.get_stripe_price_id(config), subscription.id
        )
    except ClientError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Stripe checkout session",
        )

    return UrlResponse(url=session_url)
