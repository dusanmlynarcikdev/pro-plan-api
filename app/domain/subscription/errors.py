from app.domain.errors import DomainNotFoundError, DomainValidationError


class InvalidEmailError(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionNotFoundError(DomainNotFoundError):
    def __init__(self) -> None:
        super().__init__("Subscription not found")
