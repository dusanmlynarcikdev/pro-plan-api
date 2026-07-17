from fastapi import APIRouter, BackgroundTasks, Request, status

from app.presentation.api.dependencies import (
    HandleStripeWebhookEventUseCase,
    VerifyStripeWebhookUseCase,
)

router = APIRouter()


@router.post("/stripe/webhooks", status_code=status.HTTP_204_NO_CONTENT)
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
