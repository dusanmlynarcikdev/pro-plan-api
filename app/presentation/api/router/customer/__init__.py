from fastapi import APIRouter

from .get_customer import router as get_customer_router

router = APIRouter(tags=["Customers"])
router.include_router(get_customer_router)

__all__ = ["router"]
