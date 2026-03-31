from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateOrUpdateSubscriptionCommand
from app.presentation.api.subscription.request import CreateOrUpdateRequest

router = APIRouter()


@router.post("/subscriptions", status_code=status.HTTP_204_NO_CONTENT)
async def create_or_update(
    request: CreateOrUpdateRequest,
    create_update_subscription: CreateOrUpdateSubscriptionCommand,
) -> None:
    await create_update_subscription.__call__(
        Email(request.email), request.price, request.period
    )
