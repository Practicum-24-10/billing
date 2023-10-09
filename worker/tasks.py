from datetime import datetime, timedelta
from uuid import UUID

import yookassa
from sqlalchemy import select

from database.models import Subscription, UsersSubscriptions, Payment
from message_broker.amqp import tasks_master
from worker.db import engine
from worker.models import (UserSubscriptionCreateModel,
                           AutopaymentModel,
                           CurrencyEnum,
                           AmountModel
                           )
from worker.exceptions import SubscriptionNotFound


async def create_user_subscription(*, payload: UserSubscriptionCreateModel) -> None:
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


async def create_payment(*,
                         users_subscriptions_id: UUID,
                         amount: float,
                         currency: CurrencyEnum = CurrencyEnum.RUB
                         ) -> None:
    async with engine.async_session() as session:
        stmt = select(Payment).where(Payment.users_subscriptions_id == users_subscriptions_id)  # noqa
        result = await session.execute(stmt)
        if result.first():
            return
        user_sub = await session.get(UsersSubscriptions, users_subscriptions_id)
        payment_params = AutopaymentModel(amount=AmountModel(value=amount,
                                                             currency=currency
                                                             ),
                                          capture=True,
                                          payment_method_id=user_sub.user.payment_methods[0].id,  # noqa
                                          description=user_sub.subscription.title,
                                          )
        payment_response = yookassa.Payment.create(payment_params.model_dump())

        new_payment = Payment(kassa_payment_id=payment_response.id,
                              payment_status=payment_response.status,
                              users_subscriptions_id=users_subscriptions_id,
                              )
        session.add(new_payment)
        await session.commit()
