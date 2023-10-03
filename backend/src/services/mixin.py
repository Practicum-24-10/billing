from abc import ABC
from uuid import UUID

import orjson

from backend.src.db.cache import AbstractCache
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentCard,
    PaymentModel,
    SubscriptionModel,
)


class AbstractMixin(ABC):
    pass


class MixinModel(AbstractMixin):
    def __init__(
        self, kassa: AbstractKassa, storage: AbstractStorage, cache: AbstractCache
    ):
        self.kassa = kassa
        self.storage = storage
        self.cache = cache

    async def _change_user_active(self, user_id: UUID, active: bool):
        return await self.storage.change_user_active(user_id, active)

    def _get_payment_link(self, payment: PaymentModel, details: DetailsPaymentModel):
        payment_response = self.kassa.get_new_payment(
            payment_params=payment, details=details
        )
        if payment_response:
            return payment_response.payment_page, payment_response.id
        return None, None

    async def _get_all_subscriptions_from_storage(self):
        return await self.storage.get_all_subscriptions()

    async def _get_link_from_kassa(
        self,
        users_subscriptions_id: UUID,
        payment: PaymentModel,
        details: DetailsPaymentModel,
    ) -> str | None:
        payment_response = self.kassa.get_new_payment(
            payment_params=payment, details=details
        )
        if not payment_response:
            return None
        response = await self.storage.save_new_payment(
            users_subscriptions_id=users_subscriptions_id,
            payment_id=payment_response.id,
            status=payment_response.status,
        )

        if response:
            return payment_response.payment_page
        return None

    async def _delete_user_payment_method(self, user_id: UUID, payment_method_id: UUID):
        return await self.storage.delete_user_payment_method(user_id, payment_method_id)

    async def _change_order_user_payment_method(
        self, user_id: UUID, payment_method_id: UUID
    ):
        return await self.storage.change_order_user_payment_method(
            user_id, payment_method_id
        )

    async def _add_data_to_cache(self, key: UUID, data: dict):
        return await self.cache.set(orjson.dumps(key), orjson.dumps(data))

    async def _get_data_from_cache(self, key: UUID):
        result = await self.cache.get(orjson.dumps(key))
        if result:
            return orjson.loads(result)

    async def _del_data_from_cache(self, key: UUID):
        result = await self.cache.delete(orjson.dumps(key))
        if result:
            return result

    def _check_conformation_payment(self, payment_id: str) -> PaymentCard | None:
        card = self.kassa.confirm(payment_id)
        if card:
            return card

    async def _check_and_add_new_card(
        self, card: PaymentCard, user_id: str, payment_method_id: str
    ):
        return await self.storage.add_new_payment_method(
            card, user_id, payment_method_id
        )

    async def _find_subscription(
        self, subscription_id: UUID
    ) -> SubscriptionModel | None:
        return await self.storage.find_subscription(subscription_id)

    async def _change_user_next_subscription(
        self, user_id: UUID, subscription_id: UUID
    ):
        return await self.storage.change_user_next_subscription(
            user_id, subscription_id
        )

    async def _get_user_info(self, user_id: UUID):
        user_info = await self.storage.get_user_info(user_id)
        return user_info

    async def _get_subscription(
        self, subscription_id: UUID
    ) -> SubscriptionModel | None:
        return await self.storage.find_subscription(subscription_id)

    def _safe_to_storage(self):
        pass

    async def _check_active_user_subscription(self, user_id: UUID):
        return await self.storage.check_user_active_subscription(user_id)

    async def _add_new_subscription_to_queue(
        self, user_id: UUID, subscription_id: UUID
    ):
        payment_method = await self.storage.get_user_default_payment(user_id)  # noqa
        return True
