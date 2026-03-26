class InvalidEmail(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid email")


class SubscriptionExpired(Exception):
    def __init__(self) -> None:
        super().__init__("Subscription expired")
