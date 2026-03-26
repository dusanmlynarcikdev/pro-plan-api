from dataclasses import dataclass

from pydantic import EmailStr, TypeAdapter, ValidationError

from app.domain.subscription.errors import InvalidEmail

_EMAIL_TYPE_ADAPTER = TypeAdapter(EmailStr)


@dataclass(frozen=True, slots=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        try:
            _EMAIL_TYPE_ADAPTER.validate_python(self.value)
        except ValidationError:
            raise InvalidEmail()
