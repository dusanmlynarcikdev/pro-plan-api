from app.domain.errors import ConflictDomainError, DomainError, ValidationDomainError


class CustomerAlreadyHasStripeSubscriptionError(ConflictDomainError):
    def __init__(self) -> None:
        super().__init__("Customer already has a Stripe subscription")


class CustomerIsNotLinkedToStripeError(ConflictDomainError):
    def __init__(self) -> None:
        super().__init__("Customer is not linked to Stripe")


class StripeError(DomainError):
    pass


class UnableToCreateBillingPortalSessionError(StripeError):
    def __init__(self) -> None:
        super().__init__("Unable to create billing portal session")


class UnableToCreateCheckoutSessionError(StripeError):
    def __init__(self) -> None:
        super().__init__("Unable to create checkout session")


class WebhookVerificationError(ValidationDomainError):
    def __init__(self) -> None:
        super().__init__("Invalid webhook")
