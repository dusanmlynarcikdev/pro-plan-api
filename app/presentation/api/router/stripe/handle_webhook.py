from fastapi import APIRouter, BackgroundTasks, Request, status

from app.presentation.api.dependencies import (
    HandleStripeWebhookEventUseCase,
    VerifyStripeWebhookUseCase,
)
from app.presentation.api.responses import (
    create_error_response_doc,
)

router = APIRouter()


@router.post(
    "/stripe/webhooks",
    responses={status.HTTP_400_BAD_REQUEST: create_error_response_doc()},
    status_code=status.HTTP_202_ACCEPTED,
)
async def handle_webhook(
    handle_webhook_event: HandleStripeWebhookEventUseCase,
    request: Request,
    verify_webhook: VerifyStripeWebhookUseCase,
    background_tasks: BackgroundTasks,
) -> None:
    """
    :raises WebhookVerificationError:
    """
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")

    event = await verify_webhook(payload, signature)

    background_tasks.add_task(handle_webhook_event, event)
