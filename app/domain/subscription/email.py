from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email

from app.domain.subscription.errors import InvalidEmail


@dataclass(frozen=True, slots=True)
class Email:
    """
    :raises InvalidEmail:
    """

    value: str

    def __post_init__(self) -> None:
        try:
            validated = validate_email(self.value, check_deliverability=False)
        except EmailNotValidError:
            raise InvalidEmail()

        object.__setattr__(self, "value", validated.normalized)
