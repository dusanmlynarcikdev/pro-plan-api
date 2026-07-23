import logging

from fastapi import FastAPI, Request, status
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.application.stripe.errors import StripeError
from app.domain.errors import (
    ConflictDomainError,
    DomainError,
    NotFoundDomainError,
)
from app.presentation.api.logger import log_response
from app.presentation.api.responses import ErrorResponse


def _get_domain_error_status_code(
    error: DomainError,
) -> int:
    match error:
        case ConflictDomainError():
            return status.HTTP_409_CONFLICT
        case NotFoundDomainError():
            return status.HTTP_404_NOT_FOUND
        case StripeError():
            return status.HTTP_502_BAD_GATEWAY
        case _:
            return status.HTTP_400_BAD_REQUEST


def register_domain_error_handler(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(
        _request: Request, error: DomainError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=_get_domain_error_status_code(error),
            content=ErrorResponse(detail=str(error)).model_dump(),
        )


def register_request_validation_error_handler(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request,
        error: RequestValidationError,
    ) -> JSONResponse:
        response = await request_validation_exception_handler(request, error)

        log_response(logging.WARNING, request, response)

        return response
