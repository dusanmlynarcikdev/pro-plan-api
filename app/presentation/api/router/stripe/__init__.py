from fastapi import APIRouter

from .create_billing_portal_session import router as create_billing_portal_session_route
from .create_checkout_session import router as create_checkout_session_route

router = APIRouter(tags=["Stripe"])
router.include_router(create_billing_portal_session_route)
router.include_router(create_checkout_session_route)

__all__ = ["router"]
