from app.domain.errors import DomainError


class InvalidAmount(DomainError):
    def __init__(self) -> None:
        super().__init__("Amount must be greater than 0")


class InvalidCurrency(DomainError):
    def __init__(self) -> None:
        super().__init__("Invalid currency")


class InvalidEmail(DomainError):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionCanceled(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscription canceled")


class SubscriptionExpired(DomainError):
    def __init__(self) -> None:
        super().__init__("Subscription expired")
