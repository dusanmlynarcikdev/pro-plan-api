from enum import StrEnum, auto


class StripeSubscriptionActiveStatus(StrEnum):
    ACTIVE = auto()
    TRIALING = auto()
    PAST_DUE = auto()
