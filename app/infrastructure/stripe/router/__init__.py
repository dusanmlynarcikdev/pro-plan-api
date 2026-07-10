from fastapi import APIRouter

from .checkout_session_create import router as checkout_session_create_route

router = APIRouter(tags=["Stripe"])
router.include_router(checkout_session_create_route)

__all__ = ["router"]
