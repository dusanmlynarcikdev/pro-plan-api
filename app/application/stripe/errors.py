from app.domain.errors import DomainError


class StripeCustomerIdIsMissingError(DomainError):
    def __init__(self) -> None:
        super().__init__("Stripe customer ID is missing")


class UnableToCreateBillingPortalSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create Stripe billing session")


class UnableToCreateCheckoutSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create Stripe checkout session")
