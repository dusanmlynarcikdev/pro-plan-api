from fastapi import APIRouter

from app.presentation.api.dependencies import CreateStripeCheckoutSessionUseCase
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/customers/stripe/checkout/sessions")
async def create_checkout_session(
    create_session: CreateStripeCheckoutSessionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    """
    :raises UnableToCreateCheckoutSessionError:
    """
    return UrlResponse(
        url=await create_session(
            request.customer_external_id,
            request.stripe_price_id,
            str(request.success_url),
            request.trial_days,
        )
    )
