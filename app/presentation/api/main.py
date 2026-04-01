from dotenv import load_dotenv
from fastapi import FastAPI

from .handlers import register_exception_handlers

load_dotenv(".env")

from app.presentation.api.router.health_check import router as health_check_router
from app.presentation.api.router.subscription import router as subscription_router

app = FastAPI(
    title="Pro Plan API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)

register_exception_handlers(app)

app.include_router(health_check_router)
app.include_router(subscription_router)
