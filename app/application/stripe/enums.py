from enum import StrEnum


class CheckoutSessionBillingPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"


class WebhookEventType(StrEnum):
    CUSTOMER_SUBSCRIPTION_DELETED = "customer.subscription.deleted"
    CHECKOUT_SESSION_COMPLETED = "checkout.session.completed"
