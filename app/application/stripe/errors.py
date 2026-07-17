from app.domain.errors import ConflictDomainError, DomainError, ValidationDomainError


class CustomerAlreadyHasStripeSubscriptionError(ConflictDomainError):
    def __init__(self) -> None:
        super().__init__("Customer already has a Stripe subscription")


class UnableToCreateBillingPortalSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create billing portal session")


class UnableToCreateCheckoutSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create checkout session")


class WebhookVerificationError(ValidationDomainError):
    def __init__(self) -> None:
        super().__init__("Invalid webhook")
