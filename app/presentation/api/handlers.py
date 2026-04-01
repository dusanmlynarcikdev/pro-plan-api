from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.domain.errors import (
    DomainConflictError,
    DomainError,
    DomainNotFoundError,
    DomainValidationError,
)
from app.presentation.api.responses import ErrorResponse


def _get_domain_error_status(error: DomainError) -> int:
    match error:
        case DomainConflictError():
            return status.HTTP_409_CONFLICT
        case DomainNotFoundError():
            return status.HTTP_404_NOT_FOUND
        case DomainValidationError():
            return status.HTTP_422_UNPROCESSABLE_CONTENT
        case _:
            return status.HTTP_500_INTERNAL_SERVER_ERROR


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(
        _request: Request, error: DomainError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=_get_domain_error_status(error),
            content=ErrorResponse(detail=str(error)).model_dump(exclude_none=True),
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_error_handler(
        _request: Request, error: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=jsonable_encoder(
                ErrorResponse(
                    detail="Invalid request", errors=error.errors()
                ).model_dump(exclude_none=True)
            ),
        )
