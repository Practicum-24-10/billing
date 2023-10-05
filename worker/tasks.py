from datetime import datetime, timedelta

import yookassa
from sqlalchemy import select

from database.models import Subscription, UsersSubscriptions, Payment
from message_broker.amqp import tasks_master
from worker.db import engine
from worker.models import UserSubscriptionCreateModel, AutopaymentModel, AmountModel
from worker.exceptions import SubscriptionNotFound


async def create_user_subscription(payload: UserSubscriptionCreateModel) -> None:
    async with engine.async_session() as session:
        subscription = await session.get(Subscription, payload.subscription_id)
        if not subscription:
            raise SubscriptionNotFound(f'ID = {payload.subscription_id} not found.')
        start_at = datetime.now()
        expires_at = start_at + timedelta(days=30)
        user_sub = UsersSubscriptions(user_id=payload.user_id,
                                      subscription_id=subscription.id,
                                      next_subscription_id=subscription.id,
                                      start_at=start_at,
                                      expires_at=expires_at,
                                      )
        session.add(user_sub)
        await session.commit()
        async with tasks_master() as master:
            await master.create_task('create_payment', auto_delete=True)


async def create_payment(payload: UserSubscriptionCreateModel) -> None:
    async with engine.async_session() as session:
        # 1. Проверяем, есть ли платеж у этой подписки, если есть - сворачиваемся
        stmt = select(Payment).where(Payment.users_subscriptions_id == payload.user_subscription_id)
        result = await session.execute(stmt):
        if result.first()
            return
        # 2. Отправлем запрос в юкассу на списание, ждем ответа
        payment_params = AutopaymentModel(
            amount=payload.amount,
            capture=True,
            payment_method_id='TODO',
            description='',
        )
        payment_response = yookassa.Payment.create(payment_params.model_dump())
        # 3. Создаем и сохраняем платеж в кассе
        new_payment = Payment()
        session.add(new_payment)
        await session.commit()
