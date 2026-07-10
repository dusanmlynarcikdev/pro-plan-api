from enum import StrEnum

from pydantic import BaseModel

from app.infrastructure.config import Config


class BillingPeriod(StrEnum):
    MONTHLY = "monthly"
    YEARLY = "yearly"

    def get_stripe_price_id(self, config: Config) -> str:
        match self:
            case BillingPeriod.MONTHLY:
                return config.stripe_price_id_monthly
            case BillingPeriod.YEARLY:
                return config.stripe_price_id_yearly


class CreateCheckoutSessionRequest(BaseModel):
    email: str
    billing_period: BillingPeriod
