from fastapi import APIRouter

from .create_billing_portal_session import router as create_billing_portal_session_route
from .create_checkout_session import router as create_checkout_session_route
from .handle_webhook import router as handle_webhook

_TAG = "Stripe"

public_router = APIRouter(tags=[_TAG])
public_router.include_router(handle_webhook)

router = APIRouter(tags=[_TAG])
router.include_router(create_billing_portal_session_route)
router.include_router(create_checkout_session_route)

__all__ = ["public_router", "router"]
