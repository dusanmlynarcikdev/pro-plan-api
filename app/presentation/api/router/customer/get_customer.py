from fastapi import APIRouter, status

from app.presentation.api.dependencies import GetCustomerUseCase
from app.presentation.api.responses import (
    create_error_response_doc,
)
from app.presentation.api.router.customer.responses import (
    CustomerResponse,
    CustomerStripeResponse,
    CustomerStripeSubscriptionResponse,
)

router = APIRouter()


@router.get(
    "/customers/{external_id}",
    responses={status.HTTP_404_NOT_FOUND: create_error_response_doc()},
)
async def get_customer(
    external_id: str, get_customer: GetCustomerUseCase
) -> CustomerResponse:
    """
    :raises CustomerNotFound:
    """
    customer = await get_customer(external_id)

    return CustomerResponse(
        stripe=CustomerStripeResponse(
            can_access_billing_portal=customer.can_access_stripe_billing_portal,
            subscription=CustomerStripeSubscriptionResponse(
                is_active=customer.is_stripe_subscription_active,
                is_trial=customer.is_stripe_subscription_trial,
                product_id=customer.stripe_subscription_product_id,
            )
            if customer.stripe_subscription_product_id
            else None,
        )
    )
