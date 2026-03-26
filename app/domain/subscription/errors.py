class InvalidAmount(Exception):
    def __init__(self) -> None:
        super().__init__("Amount must be greater than 0")


class InvalidCurrency(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid currency")


class InvalidEmail(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionExpired(Exception):
    def __init__(self) -> None:
        super().__init__("Subscription expired")
