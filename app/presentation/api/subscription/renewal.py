from fastapi import APIRouter, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import RenewalSubscriptionCommand

router = APIRouter()


@router.post("/subscriptions/{email}/renewal", status_code=status.HTTP_201_CREATED)
async def renewal(email: str, renewal_command: RenewalSubscriptionCommand) -> None:
    """
    :raises InvalidEmail:
    """
    await renewal_command.__call__(Email(email))
