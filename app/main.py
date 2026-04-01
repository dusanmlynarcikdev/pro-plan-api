from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.domain.errors import (
    DomainConflictError,
    DomainError,
    DomainNotFoundError,
    DomainValidationError,
)

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


def _get_domain_error_status(error: DomainError) -> int:
    match error:
        case DomainConflictError():
            return status.HTTP_409_CONFLICT
        case DomainNotFoundError():
            return status.HTTP_404_NOT_FOUND
        case DomainValidationError():
            return status.HTTP_422_UNPROCESSABLE_CONTENT
        case _:
            return status.HTTP_400_BAD_REQUEST


@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, error: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=_get_domain_error_status(error),
        content={"message": str(error)},
    )


app.include_router(health_check_router)
app.include_router(create_or_update_subscription_router, tags=["subscription"])
app.include_router(renewal_subscription_router, tags=["subscription"])
