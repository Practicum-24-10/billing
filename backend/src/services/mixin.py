import uuid
from abc import ABC
from uuid import UUID

import orjson

from backend.src.db.cache import AbstractCache
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentModel,
    PaymentResponseModel,
    SubscriptionModel,
)
from database import Subscription


class AbstractMixin(ABC):
    pass


class MixinModel(AbstractMixin):
    def __init__(self, kassa: AbstractKassa, storage: AbstractStorage,
                 cache: AbstractCache):
        self.kassa = kassa
        self.storage = storage
        self.cache = cache

    def _get_payment_link(self, payment: PaymentModel,
                          details: DetailsPaymentModel):
        payment_response = self.kassa.get_new_payment(
            payment_params=payment,
            details=details)
        if payment_response:
            return payment_response.payment_page, payment_response.id

    async def _get_link_from_kassa(self, users_subscriptions_id: UUID,
                                   payment: PaymentModel,
                                   details: DetailsPaymentModel) -> str | None:
        payment_response = self.kassa.get_new_payment(
            payment_params=payment,
            details=details)
        response = await self.storage.save_new_payment(
            users_subscriptions_id=users_subscriptions_id,
            payment_id=payment_response.id,
            status=payment_response.status)

        if response:
            return payment_response.payment_page
        return None

    async def _add_data_to_cache(self, key: UUID, data: dict):
        return await self.cache.set(orjson.dumps(key), orjson.dumps(data))

    async def _get_data_from_cache(self, key: UUID):
        result = await self.cache.get(orjson.dumps(key))
        if result:
            return orjson.loads(result)
    async def _del_data_from_cache(self, key: UUID):
        result = await self.cache.delete(orjson.dumps(key))
        if result:
            return orjson.loads(result)
    def _check_conformation_payment(self, payment_id: str):
        card = self.kassa.confirm(payment_id)
        if card:
            return card

    async def _add_subscription_for_user(self, user_id: UUID, subscription_id: UUID) -> \
            tuple[Subscription, UUID] | tuple[None, None]:
        await self.storage.add_user(user_id)
        subscription = await self.storage.find_subscription(subscription_id)
        if not subscription:
            return None, None

        user_subscription_id = await self.storage.add_subscription_to_user(user_id,
                                                                           subscription)
        if not user_subscription_id:
            return None, None
        return subscription, user_subscription_id

    async def _get_subscription(self,
                                subscription_id: UUID) -> SubscriptionModel | None:
        return await self.storage.find_subscription(subscription_id)

    def _safe_to_storage(self):
        pass

    async def _check_permissions(self, permissions: list[str]):
        subscriptions_permissions = await self.storage.get_all_subscriptions_permissions()
        result = set(permissions) & set(subscriptions_permissions)
        if result:
            return True
        return False
