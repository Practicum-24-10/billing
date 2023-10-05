from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload
from backend.src.services.subscriptions import (
    SubscriptionService,
    get_subscription_service,
)

from .models import subscriptions_api_models as api_models

router = APIRouter()


@router.get(
    "/user_info",
    response_description="All user info",
    response_model=api_models.UserInfoResponse,
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
    if user:
        return api_models.UserInfoResponse(
            id=user.id,
            active=user.active,
            subscriptions=[
                api_models.UserSubscriptionResponse(
                    id=user_subscription.id,
                    start_at=user_subscription.start_at,
                    expires_at=user_subscription.expires_at,
                    payments=[
                        api_models.UserPaymentResponse(
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
                api_models.UserPaymentMethodResponse(
                    id=payment_method.id,
                    order=payment_method.order,
                    card_type=payment_method.card_type,
                    first_numbers=payment_method.first_numbers,
                    last_numbers=payment_method.last_numbers,
                )
                for payment_method in user.payment_methods
            ],
        )
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail=errors.POSTGRES_USER_NOT_FOUND
    )


@router.get(
    "/all",
    response_description="All subscriptions",
    response_model=list[api_models.SubscriptionsResponse],
    summary="Получение всех видов подписок",
)
async def get_all_subscriptions(
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    subscriptions = await subscriptions_service.get_all_subscriptions()
    if subscriptions:
        return [
            api_models.SubscriptionsResponse(
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
    response_model=api_models.AutoRenewalResponse,
    summary="Включение/Выключение автопродления подписки",
)
async def auto_renewal(
    body: api_models.AutoRenewalModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    response = await subscriptions_service.change_auto_renewal(jwt, body.active)
    if response:
        return api_models.AutoRenewalResponse(active=response.active)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/change_next_subscription",
    response_description="Change next subscription",
    response_model=api_models.NextSubResponse,
    summary="Изменение следующей подписки",
)
async def change_next_subscription(
    body: api_models.NextSubModel,
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
        return api_models.NextSubResponse(status=response)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)


@router.post(
    "/pay_new_subscription",
    response_description="Pay new subscription",
    response_model=api_models.NewSubscriptionResponse,
    summary="Оплата подписки",
)
async def pay_new_subscriptions(
    body: api_models.NewSubscriptionModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    subscriptions_service: SubscriptionService = Depends(get_subscription_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    active_user_subscription = (
        await subscriptions_service.check_user_active_subscription(jwt)
    )
    if not active_user_subscription:
        status = await subscriptions_service.pay_subscription(
            jwt,
            body.subscription_id,
        )
        if status:
            return api_models.NewSubscriptionResponse(status=True)
    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST,
        detail=errors.POSTGRES_USER_SUBSCRIPTION_FOUND,
    )
