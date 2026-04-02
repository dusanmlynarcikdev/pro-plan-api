from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateOrUpdateSubscriptionUseCase
from app.presentation.api.router.subscription.requests import CreateOrUpdateRequest

router = APIRouter()


@router.post("/subscriptions", status_code=status.HTTP_204_NO_CONTENT)
async def create_or_update(
    request: CreateOrUpdateRequest,
    create_or_update_use_case: CreateOrUpdateSubscriptionUseCase,
) -> None:
    """
    :raises InvalidEmail:
    """
    await create_or_update_use_case(Email(request.email), request.period)
