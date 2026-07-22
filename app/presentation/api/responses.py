from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, validate_by_name=True)


class ErrorResponse(BaseResponse):
    detail: str


def create_error_response_doc(
    description: str | None = None,
) -> dict[str, str | None | type[ErrorResponse]]:
    return {
        "description": description,
        "model": ErrorResponse,
    }
