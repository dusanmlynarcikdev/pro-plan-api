from fastapi import APIRouter

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateStripeCheckoutSessionUseCase
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/checkout/sessions")
async def create_checkout_session(
    create_session: CreateStripeCheckoutSessionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    """
    :raises UnableToCreateCheckoutSessionError:
    """
    return UrlResponse(
        url=await create_session(Email(request.email), request.billing_period)
    )
