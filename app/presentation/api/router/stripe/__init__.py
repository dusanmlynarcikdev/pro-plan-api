from fastapi import APIRouter, status

from app.presentation.api.router.customer import TAG as CUSTOMER_TAG

from ...responses import create_error_response_doc
from .create_billing_portal_session import router as create_billing_portal_session_route
from .create_checkout_session import router as create_checkout_session_route
from .handle_webhook import router as handle_webhook

router = APIRouter(
    tags=[CUSTOMER_TAG],
    responses={
        status.HTTP_502_BAD_GATEWAY: create_error_response_doc(
            "Unsuccessful response from Stripe"
        )
    },
)
router.include_router(create_billing_portal_session_route)
router.include_router(create_checkout_session_route)

webhook_router = APIRouter(tags=["Stripe"])
webhook_router.include_router(handle_webhook)

__all__ = ["router", "webhook_router"]
