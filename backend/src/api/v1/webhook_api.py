# from http import HTTPStatus
#
# from fastapi import APIRouter, HTTPException, Request
# from pydantic import BaseModel, Field
# from yookassa import Configuration, Payment
# from yookassa.domain.common import SecurityHelper
# from yookassa.domain.notification import (
#     WebhookNotificationEventType,
#     WebhookNotificationFactory,
# )
#
# from backend.src.local.api import errors
#
# router = APIRouter()
#
#
# class WebhookModel(BaseModel):
#     time: int = Field(
#         title="unix timestamp",
#         description="Время",
#         example=1611039931,
#         gt=0,
#         lt=9999999999,
#     )
#
#
# class WebhookResponse(BaseModel):
#     status: bool = Field(title="Успех", example=True)
#
#
# @router.post(
#     "/webhook",
#     response_description="Webhook handler",
#     response_model=WebhookResponse,
#     summary="Адрес для автоматических уведомлений",
# )
# async def webhook_handler(request: Request, body: WebhookModel):
#     # Если хотите убедиться, что запрос пришел от ЮКасса, добавьте проверку:
#     ip = request.client.host  # Получите IP запроса
#     if not SecurityHelper().is_ip_trusted(ip):
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED
#         )
#
#     # Извлечение JSON объекта из тела запроса
#     # event_json = json.loads(body)
#     try:
#         # Создание объекта класса уведомлений в зависимости от события
#         notification_object = WebhookNotificationFactory().create(body)
#         response_object = notification_object.object
#         if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
#             some_data = {
#                 "paymentId": response_object.id,
#                 "paymentStatus": response_object.status,
#             }
#             # Специфичная логика
#             # ...
#         elif (
#             notification_object.event
#             == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE
#         ):
#             some_data = {
#                 "paymentId": response_object.id,
#                 "paymentStatus": response_object.status,
#             }
#             # Специфичная логика
#             # ...
#         elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
#             some_data = {
#                 "paymentId": response_object.id,
#                 "paymentStatus": response_object.status,
#             }
#             # Специфичная логика
#             # ...
#         elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
#             some_data = {
#                 "refundId": response_object.id,
#                 "refundStatus": response_object.status,
#                 "paymentId": response_object.payment_id,
#             }
#             # Специфичная логика
#             # ...
#         elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
#             some_data = {
#                 "dealId": response_object.id,
#                 "dealStatus": response_object.status,
#             }
#             # Специфичная логика
#             # ...
#         elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
#             some_data = {
#                 "payoutId": response_object.id,
#                 "payoutStatus": response_object.status,
#                 "dealId": response_object.deal.id,
#             }
#             # Специфичная логика
#             # ...
#         elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
#             some_data = {
#                 "payoutId": response_object.id,
#                 "payoutStatus": response_object.status,
#                 "dealId": response_object.deal.id,
#             }
#             # Специфичная логика
#             # ...
#         else:
#             # Обработка ошибок
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED
#             )  # Сообщаем кассе об ошибке
#
#         # Специфичная логика
#         # ...
#         Configuration.configure("XXXXXX", "test_XXXXXXXX")
#         # Получим актуальную информацию о платеже
#         payment_info = Payment.find_one(some_data["paymentId"])
#         if payment_info:
#             payment_status = payment_info.status
#             # Специфичная логика
#             # ...
#         else:
#             # Обработка ошибок
#             raise HTTPException(
#                 status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED
#             )  # Сообщаем кассе об ошибке
#
#     except Exception:
#         # Обработка ошибок
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED
#         )  # Сообщаем кассе об ошибке
#
#     return WebhookResponse(status=True)  # Сообщаем кассе, что все хорошо
