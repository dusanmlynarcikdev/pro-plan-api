from app.domain.errors import DomainNotFoundError, DomainValidationError


class InvalidEmail(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionNotFound(DomainNotFoundError):
    def __init__(self) -> None:
        super().__init__("Subscription not found")
