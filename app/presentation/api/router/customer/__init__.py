from fastapi import APIRouter

from .get_customer import router as get_customer_router

TAG = "Customers"

router = APIRouter(tags=[TAG])
router.include_router(get_customer_router)

__all__ = ["router"]
