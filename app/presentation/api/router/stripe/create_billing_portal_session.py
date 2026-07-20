from fastapi import APIRouter, status

from app.presentation.api.dependencies import CreateStripeBillingPortalSessionUseCase
from app.presentation.api.responses import create_error_response_doc
from app.presentation.api.router.stripe.requests import (
    CustomerRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post(
    "/stripe/billing-portal/sessions",
    responses={
        status.HTTP_404_NOT_FOUND: create_error_response_doc(),
        status.HTTP_409_CONFLICT: create_error_response_doc("Customer is not linked to Stripe")
    },
)
async def create_billing_portal_session(
    create_session: CreateStripeBillingPortalSessionUseCase,
    request: CustomerRequest,
) -> UrlResponse:
    """
    :raises CustomerIsNotLinkedToStripeError:
    :raises CustomerNotFound:
    :raises UnableToCreateBillingPortalSessionError:
    """
    return UrlResponse(url=await create_session(request.customer_external_id))
