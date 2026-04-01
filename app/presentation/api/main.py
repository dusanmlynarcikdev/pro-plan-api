from dotenv import load_dotenv
from fastapi import FastAPI

from .handlers import register_exception_handlers

load_dotenv(".env")

from app.presentation.api.health_check import router as health_check_router
from app.presentation.api.subscription.create_or_update import (
    router as create_or_update_subscription_router,
)
from app.presentation.api.subscription.renewal import (
    router as renewal_subscription_router,
)

app = FastAPI(
    title="Pro Subscription Management API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)

register_exception_handlers(app)

app.include_router(health_check_router)
app.include_router(create_or_update_subscription_router, tags=["subscription"])
app.include_router(renewal_subscription_router, tags=["subscription"])
