from app.domain.errors import NotFoundDomainError, ValidationDomainError


class InvalidEmailError(ValidationDomainError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class CustomerNotFoundError(NotFoundDomainError):
    def __init__(self) -> None:
        super().__init__("Customer not found")
