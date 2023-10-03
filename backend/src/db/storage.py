import uuid
from abc import ABC
from datetime import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import and_, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from backend.src.local.api import errors
from backend.src.models.kassa import PaymentCard, SubscriptionModel
from backend.src.models.storage import (
    AutoRenewalModel,
    UserInfoModel,
    UserPaymentMethod,
    UserPaymentModel,
    UserSubscriptionModel,
)
from database import (
    AsyncPostgres,
    Payment,
    PaymentMethod,
    Subscription,
    User,
    UsersPaymentMethods,
    UsersSubscriptions,
)


class AbstractStorage(ABC):
    async def save_new_payment(
        self, users_subscriptions_id: UUID, payment_id: str, status: str
    ):
        pass

    async def delete_user_payment_method(self, user_id: UUID, payment_method_id: UUID):
        pass

    async def change_user_active(self, user_id: UUID, active: bool) -> AutoRenewalModel | None:
        pass

    async def find_subscription(self, subscription_id: UUID) -> Subscription | None:
        pass

    async def change_user_next_subscription(self, user_id: UUID, subscription_id: UUID):
        pass

    async def get_all_subscriptions_permissions(self):
        pass

    async def add_subscription_to_user(self, user_id: UUID, subscription: Subscription):
        pass

    async def add_user(self, user_id: UUID):
        pass

    async def add_new_card(
        self, card: PaymentCard, user_id: str, payment_method_id: str
    ):
        pass

    async def change_order_user_payment_method(
        self, user_id: UUID, user_payment_method_id: UUID
    ):
        pass

    async def get_all_subscriptions(self):
        pass


    async def get_user_info(self, user_id: UUID):
        pass


class PostgresStorage(AbstractStorage):
    def __init__(self, user, password, host, port, name):
        self.driver = AsyncPostgres(user, password, host, port, name)

    async def start(self):
        await self.driver.start()

    async def end(self):
        await self.driver.close()

    async def get_user_info(self, user_id: UUID) -> UserInfoModel:
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.subscriptions).selectinload(
                        UsersSubscriptions.payment
                    ),
                    selectinload(User.payment_methods).selectinload(
                        UsersPaymentMethods.payment_method
                    ),
                )
                .filter(User.id == user_id)
            )
            user = result.scalar()
            if user:
                return UserInfoModel(
                    id=user.id,
                    active=user.active,
                    subscriptions=[
                        UserSubscriptionModel(
                            id=user_subscription.id,
                            start_at=user_subscription.start_at,
                            expires_at=user_subscription.expires_at,
                            payments=[
                                UserPaymentModel(
                                    id=payment.id,
                                    created_at=payment.created_at,
                                    payment_status=payment.payment_status,
                                )
                                for payment in user_subscription.payment
                            ],
                        )
                        for user_subscription in user.subscriptions
                    ],
                    payment_methods=[
                        UserPaymentMethod(
                            id=payment_method.id,
                            order=payment_method.order,
                            card_type=payment_method.payment_method.card_type,
                            first_numbers=payment_method.payment_method.first_numbers,
                            last_numbers=payment_method.payment_method.last_numbers,
                        )
                        for payment_method in user.payment_methods
                    ],
                )
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=errors.POSTGRES_USER_NOT_FOUND,
            )

    async def change_user_next_subscription(self, user_id: UUID, subscription_id: UUID):
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(UsersSubscriptions)
                .join(Payment, Payment.users_subscriptions_id == UsersSubscriptions.id)
                .filter(Payment.payment_status == "succeeded")
                .filter(
                    and_(
                        UsersSubscriptions.user_id == user_id,
                        UsersSubscriptions.expires_at > datetime.now(),
                    )
                )
            )
            user_subscription = result.scalars().first()
            if not user_subscription:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=errors.POSTGRES_USER_SUBSCRIPTION_NOT_FOUND,
                )
            user_subscription.next_subscription_id = subscription_id
            await session.commit()
            return True

    async def save_new_payment(
        self, users_subscriptions_id: UUID, payment_id: str, status: str
    ):
        async with self.driver.async_session() as session:
            session.add(
                Payment(
                    users_subscriptions_id=users_subscriptions_id,
                    kassa_payment_id=payment_id,
                    payment_status=status,
                )
            )
            await session.commit()
        return True

    async def change_order_user_payment_method(
        self, user_id: UUID, user_payment_method_id: UUID
    ):
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(UsersPaymentMethods).filter(
                    and_(
                        UsersPaymentMethods.id == user_payment_method_id,
                        UsersPaymentMethods.user_id == user_id,
                    )
                )
            )
            users_payment_method = result.scalars().first()
            if users_payment_method:
                new_order = await self._get_new_max_order_from_user_payment_method(
                    session, str(user_id)
                )
                users_payment_method.order = new_order
                await session.commit()
                return True
            return False

    async def change_user_active(self, user_id: UUID, active: bool) -> AutoRenewalModel | None:
        async with self.driver.async_session() as session:
            user = await self._get_user(session, user_id)
            if user:
                user.active = active
                await session.commit()
                return AutoRenewalModel(active=active)
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=errors.NO_AUTHORIZED
            )

    @staticmethod
    async def _get_user(session: AsyncSession, user_id: UUID):
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    @staticmethod
    async def _get_new_max_order_from_user_payment_method(
        session: AsyncSession, user_id: str
    ):
        result = await session.execute(
            select(func.max(UsersPaymentMethods.order)).where(
                UsersPaymentMethods.user_id == user_id
            )
        )
        max_order = result.scalar()
        if max_order is None:
            new_order = 0
        else:
            new_order = max_order + 1
        return new_order

    async def delete_user_payment_method(
        self, user_id: UUID, user_payment_method_id: UUID
    ):
        async with self.driver.async_session() as session:
            query = (
                select(UsersPaymentMethods, PaymentMethod)
                .join(
                    PaymentMethod,
                    UsersPaymentMethods.payment_method_id == PaymentMethod.id,
                )
                .where(
                    and_(
                        UsersPaymentMethods.id == user_payment_method_id,
                        UsersPaymentMethods.user_id == user_id,
                    )
                )
            )

            result = await session.execute(query)
            row = result.first()

            if row:
                users_payment_method, payment_method = row
                await session.delete(users_payment_method)
                await session.delete(payment_method)
                await session.commit()
                return True
            else:
                return False

    async def add_new_card(
        self, card: PaymentCard, user_id: str, payment_method_id: str
    ):
        async with self.driver.async_session() as session:
            new_order = await self._get_new_max_order_from_user_payment_method(
                session, user_id
            )
            result = await session.execute(
                select(PaymentMethod)
                .join(
                    UsersPaymentMethods,
                    UsersPaymentMethods.payment_method_id == PaymentMethod.id,
                )
                .join(User, User.id == UsersPaymentMethods.user_id)
                .filter(
                    PaymentMethod.card_type == card.card_type,
                    PaymentMethod.first_numbers == card.first6,
                    PaymentMethod.last_numbers == card.last4,
                )
            )
            payment_method = result.scalars().first()
            if payment_method:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND,
                    detail=errors.POSTGRES_USER_METHODE_EXISTS,
                )
            base_payment_method = uuid.uuid4()
            session.add_all(
                [
                    PaymentMethod(
                        id=base_payment_method,
                        kassa_payment_method_id=payment_method_id,
                        card_type=card.card_type,
                        first_numbers=card.first6,
                        last_numbers=card.last4,
                    ),
                    UsersPaymentMethods(
                        id=uuid.uuid4(),
                        user_id=user_id,
                        payment_method_id=base_payment_method,
                        order=new_order,
                    ),
                ]
            )
            await session.commit()
            return True

    async def find_subscription(self, subscription_id: UUID) -> Subscription | None:
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(Subscription).filter(Subscription.id == subscription_id)
            )
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
            result = await session.execute(select(User).filter(User.id == user_id))
            user = result.scalars().first()
            if not user:
                session.add(User(id=user_id, active=True))
                await session.commit()

    async def add_subscription_to_user(self, user_id: UUID, subscription: Subscription):
        async with self.driver.async_session() as session:
            user_subscription_id = uuid.uuid4()
            session.add(
                UsersSubscriptions(
                    id=user_subscription_id,
                    user_id=user_id,
                    subscription_id=subscription.id,
                    next_subscription_id=subscription.id,
                )
            )
            await session.commit()
            return user_subscription_id

    async def get_all_subscriptions_permissions(self):
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(Subscription.permission)
                .where(Subscription.active == True)
                .group_by(Subscription.permission)
            )
            permissions = result.scalars().all()
            return permissions

    async def get_all_subscriptions(self) -> list[SubscriptionModel] | None:
        async with self.driver.async_session() as session:
            result = await session.execute(
                select(Subscription).where(Subscription.active == True)
            )
            subscriptions = result.scalars().all()
            if subscriptions:
                result = [
                    SubscriptionModel(
                        id=sub.id,
                        duration=sub.duration,
                        price=sub.amount,
                        title=sub.title,
                        currency=sub.currency,
                    )
                    for sub in subscriptions
                ]
                return result
            return None

    # async def start(self):
    #     await self.driver.start()
    #
    # async def close(self):
    #     await self.driver.close()
