import json
from enum import Enum
from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, HTTPException, Request, Path
from pydantic import BaseModel, Field
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import (
    WebhookNotificationEventType,
    WebhookNotificationFactory,
)

from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload
from backend.src.services.subscriptions import (
    SubscriptionService,
    get_subscription_service,
)

router = APIRouter()


class AllSubscribesResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


class WebhookResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


class WebhookModel(BaseModel):
    time: int = Field(title="unix timestamp",
                      description="Время",
                      example=1611039931, gt=0, lt=9999999999)


class PaymentMethodEnum(str, Enum):
    bank_card = "bank_card"


class PayModel(BaseModel):
    subscription_id: UUID = Field(title="subscription_id",
                                  description="subscription_id",
                                  example="94791a79-42a0-46cc-b231-9d8f61569b47"
                                  )
    redirect_url: str = Field(title="description",
                              description="description",
                              example="https://www.example.com/return_url"
                              )
    payment_method: PaymentMethodEnum = Field(title="payment_method",
                                              description="payment_method",
                                              example="bank_card"
                                              )
    idempotence_key: UUID = Field(title="idempotence_key",
                                  description="idempotence_key",
                                  example="f39d7b6d-aef2-40b1-aaf0-cf05e7048011"
                                  )


class PaymentModel(BaseModel):
    payment_method: PaymentMethodEnum = Field(title="payment_method",
                                              description="payment_method",
                                              example="bank_card"
                                              )
    idempotence_key: UUID = Field(title="idempotence_key",
                                  description="idempotence_key",
                                  example="f39d7b6d-aef2-40b1-aaf0-cf05e7048011"
                                  )


class PayResponse(BaseModel):
    payment_link: str = Field(title="Ссылка на оплату",
                              example="https://www.example.com/return_url")


class PaymentResponse(BaseModel):
    payment_link: str = Field(title="Ссылка на оплату",
                              example="https://www.example.com/return_url")


class CancelSubModel(BaseModel):
    time: int = Field(title="unix timestamp",
                      description="Время",
                      example=1611039931, gt=0, lt=9999999999)


class CancelSubResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)

class PaymentAddResponse(BaseModel):
    status: bool = Field(title="Успех", example=True)


@router.get(
    "/all",
    response_description="All subscriptions",
    response_model=AllSubscribesResponse,
    summary="Получение всех видов подписок",
)
async def get_all_subscriptions(
        jwt: None | JWTPayload = Depends(get_token_payload),
        subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.NO_AUTHORIZED)
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
        subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=404,
            detail=errors.NO_AUTHORIZED)
    active_subscription = await subscriptions_service.check_subscription(jwt)
    if not active_subscription:
        payment_link = await subscriptions_service.pay_subscription(jwt,
                                                                    body.subscription_id,
                                                                    body.payment_method,
                                                                    body.redirect_url,
                                                                    body.idempotence_key)
        return PayResponse(payment_link=payment_link, status=True)
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=errors.NO_AUTHORIZED)


@router.post(
    "/add_payment_method",
    response_description="Pay subscription",
    response_model=PaymentResponse,
    summary="Добавление метода оплаты",
)
async def add_payment_method(
        body: PaymentModel,
        jwt: None | JWTPayload = Depends(get_token_payload),
        subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=errors.NO_AUTHORIZED)
    # active_subscription = await subscriptions_service.check_subscription(jwt)
    payment_link = await subscriptions_service.add_payment_method(jwt,
                                                                  body.payment_method,
                                                                  body.idempotence_key)
    if payment_link:
        return PaymentResponse(payment_link=payment_link)
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=errors.NO_AUTHORIZED)


@router.get(
    "/{redirect_uuid}",
    response_description="Страница редиректа",
    response_model=PaymentAddResponse,
    summary="Добавление метода оплаты",
)
async def redirect(
        redirect_uuid: Annotated[UUID, Path(
            description="redirect_uuid",
            example="77bff1a8-f6e2-4a6c-b555-b5d44c34c0dd"
        )], jwt: None | JWTPayload = Depends(get_token_payload),
        subscriptions_service: SubscriptionService = Depends(get_subscription_service)):
    # if jwt is None:
    #     raise HTTPException(
    #         status_code=HTTPStatus.UNAUTHORIZED,
    #         detail=errors.NO_AUTHORIZED)
    status = await subscriptions_service.confirm_add_payment(redirect_uuid)
    if status:
        return PaymentAddResponse(status=True)
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=errors.NO_AUTHORIZED)


@router.post(
    "/cancel",
    response_description="Сancel subscription",
    response_model=CancelSubResponse,
    summary="Отмена подписки",
)
async def cancel_subscriptions(
        body: CancelSubModel,
        jwt: None | JWTPayload = Depends(get_token_payload),
        subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=errors.NO_AUTHORIZED)
    active_subscription = await subscriptions_service.check_subscription(jwt)
    if active_subscription is not None:
        response = await subscriptions_service.cancel_subscription(jwt)
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
