from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from backend.src.db.postgres import get_postgres
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.kassa.yoo_kassa import get_yookassa
from backend.src.models.jwt import JWTPayload
from backend.src.models.kassa import DetailsPaymentModel, PaymentModel
from backend.src.services.mixin import MixinModel


class SubscriptionService(MixinModel):
    async def pay_subscription(self, jwt: JWTPayload, subscription_id: UUID,
                               payment_method: str, redirect_url: str,idempotence_key: UUID):
        user_id = jwt.user_id
        subscription = await self._get_subscription(subscription_id)
        if subscription is None:
            return None
        payment = PaymentModel(amount_value=subscription.price,
                               amount_currency=subscription.currency,
                               payment_method=payment_method,
                               redirect_url=redirect_url)
        details = DetailsPaymentModel(
            description=f"Оплата подписки {subscription.title} на {subscription.duration} дней",
            duration=subscription.duration,
            idempotence_key=idempotence_key)
        return await self._get_link_from_kassa(user_id, payment, details)

    async def cancel_subscription(self, jwt: JWTPayload):
        pass

    async def check_subscription(self, jwt: JWTPayload):
        return await self._get_active_subscription(jwt.user_id)


@lru_cache()
def get_subscription_service(
        kassa: AbstractKassa = Depends(get_yookassa),
        storage: AbstractStorage = Depends(get_postgres),
) -> SubscriptionService:
    return SubscriptionService(kassa, storage)
