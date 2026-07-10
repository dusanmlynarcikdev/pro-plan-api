from app.domain.errors import DomainError


class CheckoutError(DomainError):
    def __str__(self) -> str:
        return "Unable to create Stripe checkout session"
