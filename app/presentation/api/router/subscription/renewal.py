from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import RenewalSubscriptionUseCase
from app.presentation.api.responses import ERROR_RESPONSE_MODEL

router = APIRouter()


@router.post(
    "/subscriptions/{email}/renewal",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL,
    },
)
async def renewal(email: str, renewal_use_case: RenewalSubscriptionUseCase) -> None:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    await renewal_use_case(Email(email))
