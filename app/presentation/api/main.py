import logging

from fastapi import APIRouter, Depends, FastAPI, status

from app.presentation.api.router.customer import router as customer_router
from app.presentation.api.router.health_check import router as health_check_router
from app.presentation.api.router.stripe import (
    router as stripe_router,
)
from app.presentation.api.router.stripe import (
    webhook_router as stripe_webhook_router,
)

from .handlers import register_exception_handlers
from .responses import ERROR_RESPONSE_MODEL
from .security import check_authentication

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
)

app_logger = logging.getLogger("app")
app_logger.addHandler(handler)

app = FastAPI(
    title="Pro Plan API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)

register_exception_handlers(app)

api_router = APIRouter(prefix="/api")
api_router.include_router(health_check_router)
api_router.include_router(stripe_webhook_router)

secure_router = APIRouter(
    dependencies=[Depends(check_authentication)],
    responses={status.HTTP_401_UNAUTHORIZED: ERROR_RESPONSE_MODEL},
)
secure_router.include_router(stripe_router)
secure_router.include_router(customer_router)
api_router.include_router(secure_router)

app.include_router(api_router)
