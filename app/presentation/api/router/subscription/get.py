from datetime import date

from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import GetSubscriptionUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL
from app.presentation.api.router.subscription.responses import GetSubscriptionResponse

router = APIRouter()


@router.get(
    "/subscriptions/{email}",
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL},
)
async def get_subscription(
    email: str, get_subscription_use_case: GetSubscriptionUseCase
) -> GetSubscriptionResponse:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    subscription = await get_subscription_use_case(Email(email))

    return GetSubscriptionResponse(
        email=subscription.email.value,
        period=subscription.period,
        expires_at=subscription.expires_at,
        is_active=subscription.is_active(date.today()),
    )
