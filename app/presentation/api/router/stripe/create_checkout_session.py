from fastapi import APIRouter, HTTPException, status

from app.application.stripe.errors import CheckoutError
from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateCheckoutSessionUseCase
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/checkout-sessions")
async def create_checkout_session(
    create_checkout_session: CreateCheckoutSessionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    try:
        checkout_url = await create_checkout_session(
            Email(request.email), request.billing_period
        )
    except CheckoutError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create Stripe checkout session",
        )

    return UrlResponse(url=checkout_url)
