from abc import ABC
from uuid import UUID

from backend.src.models.kassa import SubscriptionModel
from database import AsyncPostgres


class AbstractStorage(ABC):
    async def save_new_payment(self, user_id: UUID, payment_id: str, status: str):
        pass

    async def find_subscription(self,
                                subscription_id: UUID) -> SubscriptionModel | None:
        pass


class PostgresStorage(AbstractStorage):
    # def __init__(self, user, password, host, port, name):
    #     self.driver = AsyncPostgres(user, password, host, port, name)

    async def save_new_payment(self, user_id: UUID, payment_id: str, status: str):
        return True

    async def find_subscription(self,
                                subscription_id: UUID) -> SubscriptionModel | None:
        return SubscriptionModel(
            id=str(subscription_id),
            price=200.0,
            currency="RUB",
            title="VIP",
            duration=30
        )
        pass

    # async def start(self):
    #     await self.driver.start()
    #
    # async def close(self):
    #     await self.driver.close()
