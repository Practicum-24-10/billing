import uuid
from functools import lru_cache
from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException

from backend.src.db.cache import AbstractCache
from backend.src.db.postgres import get_postgres
from backend.src.db.redis_db import get_redis
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.kassa.yoo_kassa import get_yookassa
from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentModel,
    SubscriptionModel,
)
from backend.src.models.storage import UserInfoModel
from backend.src.services.mixin import MixinModel


class SubscriptionService(MixinModel):
    async def change_next_subscription(self, jwt: JWTPayload, subscription_id: UUID):
        subscription = await self._find_subscription(subscription_id)
        if not subscription:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=errors.POSTGRES_SUBSCRIPTION_NOT_FOUND,
            )
        user_id = jwt.user_id
        return await self._change_user_next_subscription(user_id, subscription_id)

    async def get_user_info(self, jwt: JWTPayload) -> UserInfoModel:
        user_id = jwt.user_id
        return await self._get_user_info(user_id)

    async def change_auto_renewal(self, jwt: JWTPayload, active: bool):
        user_id = jwt.user_id
        return await self._change_user_active(user_id, active)

    async def pay_subscription(
        self,
        jwt: JWTPayload,
        subscription_id: UUID,
        payment_method: str,
        redirect_url: str,
        idempotence_key: UUID,
    ):
        user_id = jwt.user_id
        subscription, user_subscription_id = await self._add_subscription_for_user(
            user_id, subscription_id
        )
        if user_subscription_id is None:
            return None  # ошибка нет такой подписки
        payment = PaymentModel(
            amount_value=subscription.amount,
            amount_currency=subscription.currency,
            payment_method=payment_method,
            redirect_url=redirect_url,
        )
        details = DetailsPaymentModel(
            description=f"Оплата подписки {subscription.title} на {subscription.duration} дней",
            duration=subscription.duration,
            metadata={"user_subscription_id": str(user_subscription_id)},
            idempotence_key=user_subscription_id,
        )
        return await self._get_link_from_kassa(user_subscription_id, payment, details)

    async def get_all_subscriptions(self) -> list[SubscriptionModel] | None:
        return await self._get_all_subscriptions_from_storage()

    async def cancel_subscription(self, jwt: JWTPayload):
        pass

    async def check_subscription(self, jwt: JWTPayload):
        return await self._check_permissions(jwt.permissions)


@lru_cache()
def get_subscription_service(
    kassa: AbstractKassa = Depends(get_yookassa),
    storage: AbstractStorage = Depends(get_postgres),
    cache: AbstractCache = Depends(get_redis),
) -> SubscriptionService:
    return SubscriptionService(kassa, storage, cache)
