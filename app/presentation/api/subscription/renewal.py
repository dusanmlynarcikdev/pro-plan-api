from fastapi import APIRouter, Response, status

from app.domain.subscription.email import Email
from app.presentation.api.dependencies import RenewalSubscriptionCommand
from app.presentation.api.responses import ERROR_RESPONSE_MODEL

router = APIRouter()


@router.post(
    "/subscriptions/{email}/renewal",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_404_NOT_FOUND: ERROR_RESPONSE_MODEL,
    },
)
async def renewal(email: str, renewal_command: RenewalSubscriptionCommand) -> Response:
    """
    :raises InvalidEmail:
    :raises SubscriptionNotFound:
    """
    await renewal_command(Email(email))

    return Response(status_code=status.HTTP_201_CREATED)
