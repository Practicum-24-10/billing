from datetime import datetime
from enum import Enum
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload
from backend.src.services.subscriptions import (
    SubscriptionService,
    get_subscription_service,
)

from .models.subscriptions_api_models import *

router = APIRouter()


@router.get(
    "/user_info",
    response_description="All user info",
    response_model=UserInfoResponse,
    summary="Все данные пользователя",
)
async def user_info(
    jwt: None | JWTPayload = Depends(get_token_payload),
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    user = await subscriptions_service.get_user_info(jwt)
    return UserInfoResponse(
        id=user.id,
        active=user.active,
        subscriptions=[
            UserSubscriptionResponse(
                id=user_subscription.id,
                start_at=user_subscription.start_at,
                expires_at=user_subscription.expires_at,
                payments=[
                    UserPaymentResponse(
                        id=payment.id,
                        created_at=payment.created_at,
                        payment_status=payment.payment_status,
                    )
                    for payment in user_subscription.payments
                ],
            )
            for user_subscription in user.subscriptions
        ],
        payment_methods=[
            UserPaymentMethodResponse(
                id=payment_method.id,
                order=payment_method.order,
                card_type=payment_method.card_type,
                first_numbers=payment_method.first_numbers,
                last_numbers=payment_method.last_numbers,
            )
            for payment_method in user.payment_methods
        ],
    )


@router.get(
    "/all",
    response_description="All subscriptions",
    response_model=list[SubscriptionsResponse],
    summary="Получение всех видов подписок",
)
async def get_all_subscriptions(
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    subscriptions = await subscriptions_service.get_all_subscriptions()
    if subscriptions:
        return [
            SubscriptionsResponse(
                id=sub.id,
                duration=sub.duration,
                price=sub.price,
                title=sub.title,
                currency=sub.currency,
            )
            for sub in subscriptions
        ]
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND)


@router.post(
    "/auto_renewal",
    response_description="On/Off auto renewal",
    response_model=AutoRenewalResponse,
    summary="Включение/Выключение автопродления подписки",
)
async def auto_renewal(
    body: AutoRenewalModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    response = await subscriptions_service.change_auto_renewal(jwt, body.active)
    if response:
        return AutoRenewalResponse(active=response.active)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/change_next_subscription",
    response_description="Change next subscription",
    response_model=NextSubResponse,
    summary="Изменение следующей подписки",
)
async def change_next_subscription(
    body: NextSubModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    response = await subscriptions_service.change_next_subscription(
        jwt, body.subscription_id
    )
    if response:
        return NextSubResponse(status=response)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


# @router.post(
#     "/pay",
#     response_description="Pay subscription",
#     response_model=PayResponse,
#     summary="Оплата подписки",
# )
# async def pay_subscriptions(
#     body: PayModel,
#     jwt: None | JWTPayload = Depends(get_token_payload),
#     subscriptions_service: SubscriptionService = Depends(get_subscription_service),
# ):
#     if jwt is None:
#         raise HTTPException(
#             status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
#         )
#     active_subscription = await subscriptions_service.check_subscription(jwt)
#     if not active_subscription:
#         payment_link = await subscriptions_service.pay_subscription(
#             jwt,
#             body.subscription_id,
#             body.payment_method,
#             body.redirect_url,
#             body.idempotence_key,
#         )
#         return PayResponse(payment_link=payment_link, status=True)
#     raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED)
#
#
# @router.post(
#     "/cancel",
#     response_description="Сancel subscription",
#     response_model=CancelSubResponse,
#     summary="Отмена подписки",
# )
# async def cancel_subscriptions(
#     body: CancelSubModel,
#     jwt: None | JWTPayload = Depends(get_token_payload),
#     subscriptions_service: SubscriptionService = Depends(get_subscription_service),
# ):
#     if jwt is None:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail=errors.NO_AUTHORIZED
#         )
#     active_subscription = await subscriptions_service.check_subscription(jwt)
#     if active_subscription is not None:
#         response = await subscriptions_service.cancel_subscription(jwt)
#     return CancelSubResponse(status=True)
