from fastapi import APIRouter, status

from ...responses import ERROR_RESPONSE_MODEL
from .create_billing_portal_session import router as create_billing_portal_session_route
from .create_checkout_session import router as create_checkout_session_route
from .handle_webhook import router as handle_webhook

TAG = "Stripe"

router = APIRouter(
    tags=[TAG], responses={status.HTTP_500_INTERNAL_SERVER_ERROR: ERROR_RESPONSE_MODEL}
)
router.include_router(create_billing_portal_session_route)
router.include_router(create_checkout_session_route)

webhook_router = APIRouter(
    tags=[TAG], responses={status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE_MODEL}
)
webhook_router.include_router(handle_webhook)

__all__ = ["router", "webhook_router"]
