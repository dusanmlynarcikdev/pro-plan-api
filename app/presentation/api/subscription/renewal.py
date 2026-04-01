from fastapi import APIRouter, Response, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import RenewalSubscriptionCommand

router = APIRouter()


@router.post("/subscriptions/{email}/renewal", status_code=status.HTTP_201_CREATED)
async def renewal(email: str, renewal_command: RenewalSubscriptionCommand) -> Response:
    """
    :raises InvalidEmail:
    """
    await renewal_command.__call__(Email(email))

    return Response(status_code=status.HTTP_201_CREATED)
