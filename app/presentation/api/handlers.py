from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.application.stripe.errors import StripeError
from app.domain.errors import (
    ConflictDomainError,
    DomainError,
    NotFoundDomainError,
    ValidationDomainError,
)
from app.presentation.api.responses import ErrorResponse


def _get_domain_error_status(error: DomainError) -> int:
    match error:
        case ConflictDomainError():
            return status.HTTP_409_CONFLICT
        case NotFoundDomainError():
            return status.HTTP_404_NOT_FOUND
        case StripeError():
            return status.HTTP_502_BAD_GATEWAY
        case ValidationDomainError():
            return status.HTTP_400_BAD_REQUEST
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR


def register_domain_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(
        _request: Request, error: DomainError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=_get_domain_error_status(error),
            content=ErrorResponse(detail=str(error)).model_dump(),
        )
