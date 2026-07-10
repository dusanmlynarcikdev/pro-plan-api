from fastapi import APIRouter, status

from app.presentation.api.responses import ERROR_RESPONSE_MODEL

from .get_subscription import router as get_subscription_router

router = APIRouter(
    tags=["Subscriptions"],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE_MODEL},
)
router.include_router(get_subscription_router)

__all__ = ["router"]
