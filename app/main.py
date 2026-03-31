from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.errors import DomainError

load_dotenv(".env")

from app.presentation.api.health_check import router as health_check_router
from app.presentation.api.subscription.subscription import router as subscription_router

app = FastAPI(
    title="Pro Subscription Management API",
    servers=[
        {"url": "http://localhost", "description": "Local"},
    ],
    swagger_ui_parameters={"operationsSorter": "alpha"},
)

app.include_router(health_check_router)
app.include_router(subscription_router)


@app.exception_handler(DomainError)
async def domain_exception_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": str(exc)},
    )
