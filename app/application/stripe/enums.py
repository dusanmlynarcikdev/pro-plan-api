from enum import StrEnum, auto


class SubscriptionMetadataKey(StrEnum):
    CUSTOMER_ID = auto()


class WebhookEventType(StrEnum):
    CUSTOMER_SUBSCRIPTION_CREATED = "customer.subscription.created"
    CUSTOMER_SUBSCRIPTION_UPDATED = "customer.subscription.updated"
    CUSTOMER_SUBSCRIPTION_DELETED = "customer.subscription.deleted"
