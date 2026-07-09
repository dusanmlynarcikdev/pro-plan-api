from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import GetSubscriptionUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL
from app.presentation.api.router.subscription.responses import SubscriptionResponse

router = APIRouter()


@router.get(
    "/subscriptions/{email}",
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL},
)
async def get_subscription(
    email: str, get_use_case: GetSubscriptionUseCase
) -> SubscriptionResponse:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    subscription = await get_use_case(Email(email))

    return SubscriptionResponse(
        id=subscription.id,
        email=subscription.email.value,
        is_active=subscription.is_active,
    )
