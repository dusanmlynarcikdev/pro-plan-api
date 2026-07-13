from app.domain.errors import DomainError


class CheckoutError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create Stripe checkout session")
