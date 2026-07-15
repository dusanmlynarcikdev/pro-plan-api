from enum import StrEnum


class BillingPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class WebhookEventType(StrEnum):
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
