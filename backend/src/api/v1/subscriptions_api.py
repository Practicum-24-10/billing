import json
from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationEventType, \
    WebhookNotificationFactory
from yookassa.domain.common import SecurityHelper

from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload

router = APIRouter()


class AllSubscribesResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


class WebhookResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


class WebhookModel(BaseModel):
    time: int = Field(title="unix timestamp",
                      description="Время",
                      example=1611039931, gt=0, lt=9999999999)


class PayModel(BaseModel):
    time: int = Field(title="unix timestamp",
                      description="Время",
                      example=1611039931, gt=0, lt=9999999999)


class PayResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


class CancelSubModel(BaseModel):
    time: int = Field(title="unix timestamp",
                      description="Время",
                      example=1611039931, gt=0, lt=9999999999)


class CancelSubResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


@router.get(
    "/all",
    response_description="All subscriptions",
    response_model=AllSubscribesResponse,
    summary="Получение всех видов подписок",
)
async def get_all_subscriptions(
        jwt: None | JWTPayload = Depends(get_token_payload),
):
    return AllSubscribesResponse(status=True)


@router.post(
    "/pay",
    response_description="Pay subscription",
    response_model=PayResponse,
    summary="Оплата подписки",
)
async def pay_subscriptions(
        body: PayModel,
        jwt: None | JWTPayload = Depends(get_token_payload),
):
    return PayResponse(status=True)


@router.post(
    "/cancel",
    response_description="Сancel subscription",
    response_model=CancelSubResponse,
    summary="Отмена подписки",
)
async def pay_subscriptions(
        body: CancelSubModel,
        jwt: None | JWTPayload = Depends(get_token_payload),
):
    return CancelSubResponse(status=True)


@router.post(
    "/webhook",
    response_description="Webhook handler",
    response_model=WebhookResponse,
    summary="Адрес для автоматических уведомлений",
)
async def webhook_handler(
        request: Request,
        body: WebhookModel):
    # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
    ip = request.client.host  # Получите IP запроса
    if not SecurityHelper().is_ip_trusted(ip):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors.NO_AUTHORIZED)

    # Извлечение JSON объекта из тела запроса
    # event_json = json.loads(body)
    try:
        # Создание объекта класса уведомлений в зависимости от события
        notification_object = WebhookNotificationFactory().create(body)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            some_data = {
                'refundId': response_object.id,
                'refundStatus': response_object.status,
                'paymentId': response_object.payment_id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
            some_data = {
                'dealId': response_object.id,
                'dealStatus': response_object.status,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=errors.NO_AUTHORIZED)  # Сообщаем кассе об ошибке

        # Специфичная логика
        # ...
        Configuration.configure('XXXXXX', 'test_XXXXXXXX')
        # Получим актуальную информацию о платеже
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
            # Специфичная логика
            # ...
        else:
            # Обработка ошибок
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=errors.NO_AUTHORIZED)  # Сообщаем кассе об ошибке

    except Exception:
        # Обработка ошибок
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=errors.NO_AUTHORIZED)  # Сообщаем кассе об ошибке

    return WebhookResponse(status=True)  # Сообщаем кассе, что все хорошо
