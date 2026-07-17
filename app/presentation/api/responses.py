from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str


def create_error_response_doc(
    description: str | None = None,
) -> dict[str, str | None | type[ErrorResponse]]:
    return {
        "description": description,
        "model": ErrorResponse,
    }
