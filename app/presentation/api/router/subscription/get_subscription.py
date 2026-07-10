from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription
from app.presentation.api.dependencies import GetSubscriptionUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL
from app.presentation.api.router.subscription.responses import SubscriptionResponse

router = APIRouter()


@router.get(
    "/subscriptions/{email}",
    response_model=SubscriptionResponse,
    responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL},
)
async def get_subscription(
    email: str, get_subscription: GetSubscriptionUseCase
) -> Subscription:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    return await get_subscription(Email(email))
