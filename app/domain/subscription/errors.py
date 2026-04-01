from app.domain.errors import (
    DomainConflictError,
    DomainNotFoundError,
    DomainValidationError,
)


class InvalidAmount(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Amount must be greater than 0")


class InvalidCurrency(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid currency")


class InvalidEmail(DomainValidationError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionCanceled(DomainConflictError):
    def __init__(self) -> None:
        super().__init__("Subscription canceled")


class SubscriptionExpired(DomainConflictError):
    def __init__(self) -> None:
        super().__init__("Subscription expired")


class SubscriptionNotFound(DomainNotFoundError):
    def __init__(self) -> None:
        super().__init__("Subscription not found")
