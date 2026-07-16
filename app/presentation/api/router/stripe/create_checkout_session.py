from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateStripeCheckoutSessionUseCase
from app.presentation.api.responses import ErrorResponse
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post(
    "/stripe/checkout/sessions",
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "Subscription is already active in Stripe",
            "model": ErrorResponse,
        }
    },
)
async def create_checkout_session(
    create_session: CreateStripeCheckoutSessionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    """
    :raises SubscriptionActiveInStripeError:
    :raises UnableToCreateCheckoutSessionError:
    """
    return UrlResponse(
        url=await create_session(Email(request.email), request.billing_period)
    )
