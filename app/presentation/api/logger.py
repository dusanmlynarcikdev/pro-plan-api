import logging

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def log_response(level: int, request: Request, response: JSONResponse) -> None:
    logger.log(
        level,
        "%s %s %s %s",
        request.method,
        request.url.path,
        response.status_code,
        bytes(response.body).decode(),
    )
