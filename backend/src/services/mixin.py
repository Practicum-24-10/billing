from abc import ABC
from uuid import UUID

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
    def __init__(self, kassa: AbstractKassa, storage: AbstractStorage):
        self.kassa = kassa
        self.storage = storage

    async def _get_link_from_kassa(self, user_id: UUID,
                                   payment: PaymentModel,
                                   details: DetailsPaymentModel) -> str | None:
        payment_response = self.kassa.get_new_payment(user_id=user_id,
                                                      payment_params=payment,
                                                      details=details)
        response = await self.storage.save_new_payment(user_id=user_id,
                                                       payment_id=payment_response.id,
                                                       status=payment_response.status)

        if response:
            return payment_response.payment_page
        return None

    async def _add_subscription_for_user(self, user_id: UUID, subscription_id: UUID):
        await self.storage.add_user(user_id)
        subscription = await self.storage.find_subscription(subscription_id)
        if not subscription:
            return None

        user_subscription = await self.storage.add_subscription_to_user(user_id,subscription)

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
