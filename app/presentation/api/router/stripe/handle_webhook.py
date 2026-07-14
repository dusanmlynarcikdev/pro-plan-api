from fastapi import APIRouter, BackgroundTasks, Request, status

from app.presentation.api.dependencies import (
    HandleWebhookEventUseCase,
    VerifyWebhookUseCase,
)

router = APIRouter()


@router.post("/stripe/webhooks", status_code=status.HTTP_204_NO_CONTENT)
async def handle_webhook(
    handle_webhook_event: HandleWebhookEventUseCase,
    request: Request,
    verify_webhook: VerifyWebhookUseCase,
    background_tasks: BackgroundTasks,
) -> None:
    """
    :raises WebhookVerificationError:
    """
    payload = await request.body()
    signature = request.headers.get("stripe-signature", "")

    event = await verify_webhook(payload, signature)
    background_tasks.add_task(handle_webhook_event.__call__, event)

    pass
