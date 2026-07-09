from fastapi import APIRouter

from app.domain.subscription.email import Email
from app.domain.subscription.subscription import Subscription
from app.presentation.api.dependencies import CreateOrGetSubscriptionUseCase
from app.presentation.api.router.subscription.requests import CreateOrGetRequest
from app.presentation.api.router.subscription.responses import IdResponse

router = APIRouter()


@router.post("/subscriptions", response_model=IdResponse)
async def create_or_get_subscription(
    request: CreateOrGetRequest,
    create_or_get_use_case: CreateOrGetSubscriptionUseCase,
) -> Subscription:
    """
    :raises InvalidEmail:
    """
    return await create_or_get_use_case(Email(request.email))
