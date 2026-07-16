from app.domain.errors import NotFoundDomainError, ValidationDomainError


class InvalidEmailError(ValidationDomainError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionNotFoundError(NotFoundDomainError):
    def __init__(self) -> None:
        super().__init__("Subscription not found")
