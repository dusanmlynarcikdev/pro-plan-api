from fastapi import FastAPI

from app.presentation.api.health_check import router as health_check_router

app = FastAPI(
    title="Pro Subscription Management REST API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)
app.include_router(health_check_router)
