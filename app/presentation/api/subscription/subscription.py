from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import CreateUpdateSubscriptionCommandDependency
from app.presentation.api.subscription.create_update_request import CreateUpdateRequest

router = APIRouter()


@router.post("/subscriptions", status_code=status.HTTP_204_NO_CONTENT)
async def create_or_update(
    request: CreateUpdateRequest,
    create_update_subscription: CreateUpdateSubscriptionCommandDependency,
) -> None:
    await create_update_subscription.__call__(
        Email(request.email), request.price, request.period
    )
