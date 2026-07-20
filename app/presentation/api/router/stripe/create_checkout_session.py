from fastapi import APIRouter, status

from app.presentation.api.dependencies import CreateStripeCheckoutSessionUseCase
from app.presentation.api.responses import create_error_response_doc
from app.presentation.api.router.stripe.requests import (
    CreateCheckoutSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post(
    "/customers/stripe/checkout/sessions",
    responses={
        status.HTTP_409_CONFLICT: create_error_response_doc(
            "Customer already has a Stripe subscription"
        )
    },
)
async def create_checkout_session(
    create_session: CreateStripeCheckoutSessionUseCase,
    request: CreateCheckoutSessionRequest,
) -> UrlResponse:
    """
    :raises CustomerAlreadyHasStripeSubscriptionError:
    :raises UnableToCreateCheckoutSessionError:
    """
    return UrlResponse(
        url=await create_session(
            request.billing_period,
            request.customer_external_id,
            str(request.success_url),
        )
    )
