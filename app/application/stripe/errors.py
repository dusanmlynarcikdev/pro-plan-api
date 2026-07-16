from app.domain.errors import ConflictDomainError, DomainError, ValidationDomainError


class SubscriptionActiveInStripeError(ConflictDomainError):
    def __init__(self) -> None:
        super().__init__("Subscription is already active in Stripe")


class UnableToCreateBillingPortalSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create billing portal session")


class UnableToCreateCheckoutSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create checkout session")


class WebhookVerificationError(ValidationDomainError):
    def __init__(self) -> None:
        super().__init__("Invalid webhook")
