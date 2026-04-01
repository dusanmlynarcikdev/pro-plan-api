from fastapi import APIRouter, status

from app.presentation.api.responses import ERROR_RESPONSE_MODEL

from .create_or_update import router as create_or_update_router
from .renewal import router as renewal_router

router = APIRouter(
    tags=["subscription"],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE_MODEL},
)
router.include_router(create_or_update_router)
router.include_router(renewal_router)

__all__ = ["router"]
