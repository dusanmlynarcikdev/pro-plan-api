from fastapi import APIRouter

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateBillingPortalSessionUseCase
from app.presentation.api.router.stripe.requests import (
    CreateBillingPortalSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/billing-portal/sessions")
async def create_billing_portal_session(
    create_billing_portal_session: CreateBillingPortalSessionUseCase,
    request: CreateBillingPortalSessionRequest,
) -> UrlResponse:
    """
    :raises StripeCustomerIdIsMissingError:
    :raises SubscriptionNotFound:
    :raises UnableToCreateBillingPortalSessionError:
    """
    return UrlResponse(url=await create_billing_portal_session(Email(request.email)))
