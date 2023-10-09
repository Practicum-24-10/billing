import json
from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)

from backend.src.local.api import errors
from backend.src.services.webhook import WebhookService, get_webhook_service

router = APIRouter()


class WebhookResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


@router.post(
    "/webhook",
    response_description="Webhook handler",
    response_model=WebhookResponse,
    summary="Адрес для автоматических уведомлений",
)
async def webhook_handler(
        request: Request,
        webhook_service: WebhookService = Depends(get_webhook_service),
):
    ip = request.client.host
    if not SecurityHelper().is_ip_trusted(ip):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED
        )
    payload = await request.body()
    event_json = json.loads(payload)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == \
                WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif (
                notification_object.event ==
                WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE
        ):
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif notification_object.event == \
                WebhookNotificationEventType.PAYMENT_CANCELED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif notification_object.event == \
                WebhookNotificationEventType.REFUND_SUCCEEDED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif notification_object.event == \
                WebhookNotificationEventType.DEAL_CLOSED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif notification_object.event == \
                WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        elif notification_object.event == \
                WebhookNotificationEventType.PAYOUT_CANCELED:
            data = {
                "paymentId": response_object.object.id,
                "paymentStatus": response_object.object.status,
                "saved": response_object.payment_method.saved,
                "metadata": response_object.metadata
            }
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST
            )
        status = await webhook_service.confirm_webhook(data)
        if status:
            return WebhookResponse(status=True)
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST
            )

    except Exception:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST
        )
