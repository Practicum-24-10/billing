import uuid
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from backend.src.db.cache import AbstractCache
from backend.src.db.postgres import get_postgres
from backend.src.db.redis_db import get_redis
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.kassa.yoo_kassa import get_yookassa
from backend.src.models.jwt import JWTPayload
from backend.src.models.kassa import DetailsPaymentModel, PaymentModel
from backend.src.services.mixin import MixinModel


class SubscriptionService(MixinModel):
    async def pay_subscription(self, jwt: JWTPayload, subscription_id: UUID,
                               payment_method: str, redirect_url: str,
                               idempotence_key: UUID):
        user_id = jwt.user_id
        subscription, user_subscription_id = await self._add_subscription_for_user(
            user_id, subscription_id)
        if user_subscription_id is None:
            return None  # ошибка нет такой подписки
        payment = PaymentModel(amount_value=subscription.amount,
                               amount_currency=subscription.currency,
                               payment_method=payment_method,
                               redirect_url=redirect_url)
        details = DetailsPaymentModel(
            description=f"Оплата подписки {subscription.title} на {subscription.duration} дней",
            duration=subscription.duration,
            metadata={"user_subscription_id": str(user_subscription_id)},
            idempotence_key=user_subscription_id)
        return await self._get_link_from_kassa(user_subscription_id, payment, details)

    async def confirm_add_payment(self, redirect_uuid):
        data = await self._get_data_from_cache(redirect_uuid)
        if not data:
            return None
        card = self._check_conformation_payment(data["payment_id"])
        if not card:
            return None
        return True

    async def cancel_subscription(self, jwt: JWTPayload):
        pass

    async def add_payment_method(self, jwt: JWTPayload, payment_method: str,
                                 idempotence_key: UUID):
        user_id = jwt.user_id
        redirect_uuid = uuid.uuid4()
        payment = PaymentModel(amount_value=1,
                               amount_currency="RUB",
                               payment_method=payment_method,
                               redirect_url=f"http://localhost:8000/api/v1/subscription/{str(redirect_uuid)}",
                               save_payment=True)
        details = DetailsPaymentModel(
            description="Привязка карты",
            metadata={"user_id": str(user_id), "cancel": True},
            idempotence_key=idempotence_key)
        payment_link, payment_id = self._get_payment_link(payment, details)
        if payment_link:
            status = await self._add_data_to_cache(redirect_uuid,
                                                   {"user_id": str(user_id),
                                                    "payment_id": payment_id})
            if status:
                return payment_link

    async def check_subscription(self, jwt: JWTPayload):
        return await self._check_permissions(jwt.permissions)


@lru_cache()
def get_subscription_service(
        kassa: AbstractKassa = Depends(get_yookassa),
        storage: AbstractStorage = Depends(get_postgres),
        cache: AbstractCache = Depends(get_redis),
) -> SubscriptionService:
    return SubscriptionService(kassa, storage, cache)
