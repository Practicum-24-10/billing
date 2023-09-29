import uuid
from abc import ABC
from datetime import datetime
from uuid import UUID

from sqlalchemy import select

from backend.src.models.kassa import SubscriptionModel, PaymentCard
from database import AsyncPostgres, Subscription, UsersSubscriptions, User, Payment, \
    PaymentMethod, UsersPaymentMethods


class AbstractStorage(ABC):
    async def save_new_payment(self, users_subscriptions_id: UUID, payment_id: str,
                               status: str):
        pass

    async def find_subscription(self,
                                subscription_id: UUID) -> Subscription | None:
        pass

    async def get_all_subscriptions_permissions(self):
        pass

    async def add_subscription_to_user(self, user_id: UUID, subscription: Subscription):
        pass

    async def add_user(self, user_id: UUID):
        pass

    async def add_new_card(self, card: PaymentCard, user_id: str,
                           payment_method_id: str):
        pass


class PostgresStorage(AbstractStorage):
    def __init__(self, user, password, host, port, name):
        self.driver = AsyncPostgres(user, password, host, port, name)

    async def start(self):
        await self.driver.start()

    async def end(self):
        await self.driver.close()

    async def save_new_payment(self, users_subscriptions_id: UUID, payment_id: str,
                               status: str):
        async with self.driver.async_session() as session:
            session.add(Payment(users_subscriptions_id=users_subscriptions_id,
                                kassa_payment_id=payment_id, payment_status=status))
            await session.commit()
        return True

    async def add_new_card(self, card: PaymentCard, user_id: str,
                           payment_method_id: str):
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(PaymentMethod)
                .join(UsersPaymentMethods,
                      UsersPaymentMethods.payment_method_id == PaymentMethod.id)
                .join(User, User.id == UsersPaymentMethods.user_id).filter(
                    PaymentMethod.card_type == card.card_type,
                    PaymentMethod.first_numbers == card.first6,
                    PaymentMethod.last_numbers == card.last4))
            payment_method = result.scalars().first()
            if payment_method:
                return False
            base_payment_method = uuid.uuid4()
            session.add_all([PaymentMethod(
                id=base_payment_method,
                kassa_payment_method_id=payment_method_id,
                card_type=card.card_type,
                first_numbers=card.first6,
                last_numbers=card.last4), UsersPaymentMethods(user_id=user_id,
                                                              payment_method_id=base_payment_method,
                                                              order=0)])
            await session.commit()
            return True

    async def find_subscription(self,
                                subscription_id: UUID) -> Subscription | None:
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(Subscription).filter(Subscription.id == subscription_id))
            subscription = result.scalars().first()
            if subscription:
                return subscription
                # return SubscriptionModel(
                #     id=subscription.id,
                #     price=subscription.amount,
                #     currency=subscription.currency,
                #     title=subscription.title,
                #     duration=subscription.duration
                # )
            return None

    async def add_user(self, user_id: UUID):
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(User).filter(User.id == user_id))
            user = result.scalars().first()
            if not user:
                session.add(User(id=user_id, active=True))
                await session.commit()

    async def add_subscription_to_user(self, user_id: UUID, subscription: Subscription):
        async with self.driver.async_session() as session:
            user_subscription_id = uuid.uuid4()
            session.add(UsersSubscriptions(id=user_subscription_id, user_id=user_id,
                                           subscription_id=subscription.id,
                                           next_subscription_id=subscription.id))
            await session.commit()
            return user_subscription_id

    async def get_all_subscriptions_permissions(self):
        async with self.driver.async_session() as session:
            result = await session.execute(select(Subscription.permission).where(
                Subscription.active == True).group_by(Subscription.permission))
            permissions = result.scalars().all()
            return permissions

    # async def start(self):
    #     await self.driver.start()
    #
    # async def close(self):
    #     await self.driver.close()
