class SubscriptionExpired(Exception):
    def __init__(self) -> None:
        super().__init__("Subscription expired")
