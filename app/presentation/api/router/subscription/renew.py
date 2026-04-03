from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import RenewSubscriptionUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL

router = APIRouter()


@router.post(
    "/subscriptions/{email}/renew",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL,
    },
)
async def renew(email: str, renew_use_case: RenewSubscriptionUseCase) -> None:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    await renew_use_case(Email(email))
