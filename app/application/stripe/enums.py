from enum import StrEnum


class SubscriptionMetadata(StrEnum):
    CUSTOMER_ID = "customer_id"


class WebhookEventType(StrEnum):
    CUSTOMER_SUBSCRIPTION_CREATED = "customer.subscription.created"
    CUSTOMER_SUBSCRIPTION_DELETED = "customer.subscription.deleted"
