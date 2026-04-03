from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel


class ErrorResponseItem(BaseModel):
    type: str
    loc: Sequence[str | int]
    msg: str
    input: Any | None = None
    ctx: dict[str, Any] | None = None
    url: str | None = None


class ErrorResponse(BaseModel):
    detail: str
    errors: Sequence[ErrorResponseItem] | None = None


ERROR_RESPONSE_MODEL = {"model": ErrorResponse}
