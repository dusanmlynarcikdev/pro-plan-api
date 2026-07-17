from fastapi import APIRouter, status

from app.presentation.api.responses import ERROR_RESPONSE_MODEL

from .get_customer import router as get_customer_router

router = APIRouter(
    tags=["Customers"],
    responses={status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE_MODEL},
)
router.include_router(get_customer_router)

__all__ = ["router"]
