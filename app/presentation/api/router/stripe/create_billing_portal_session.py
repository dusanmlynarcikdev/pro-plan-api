from fastapi import APIRouter

from app.presentation.api.router.stripe.requests import (
    CreateBillingPortalSessionRequest,
)
from app.presentation.api.router.stripe.responses import UrlResponse

router = APIRouter()


@router.post("/stripe/billing-portal/sessions")
async def create_billing_portal_session(
    request: CreateBillingPortalSessionRequest,
) -> UrlResponse: ...
