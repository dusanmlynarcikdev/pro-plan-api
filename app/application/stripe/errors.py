from app.domain.errors import DomainError


class UnableToCreateBillingPortalSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create billing portal session")


class UnableToCreateCheckoutSessionError(DomainError):
    def __init__(self) -> None:
        super().__init__("Unable to create checkout session")


class WebhookVerificationError(Exception):
    def __init__(self) -> None:
        super().__init__("An error occurred while verifying webhook")
