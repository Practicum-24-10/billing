from sqlalchemy import delete

from database import (
    Payment,
    PaymentMethod,
    Subscription,
    User,
    UsersPaymentMethods,
    UsersSubscriptions,
)


async def delete_all(pg_client):
    async with pg_client.async_session() as session:
        await session.execute(delete(UsersPaymentMethods))
        await session.execute(delete(PaymentMethod))
        await session.execute(delete(Payment))
        await session.execute(delete(UsersSubscriptions))
        await session.execute(delete(Subscription))
        await session.execute(delete(User))
        await session.commit()
