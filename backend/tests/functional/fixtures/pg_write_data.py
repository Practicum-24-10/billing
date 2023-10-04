import pytest

from backend.tests.functional import testdata
from backend.tests.functional.utils.utils import delete_all
from database import (
    Payment,
    PaymentMethod,
    Subscription,
    User,
    UsersPaymentMethods,
    UsersSubscriptions,
)


@pytest.fixture
def pg_write_data(pg_client):
    async def inner():
        async with pg_client.async_session() as session:
            users = [User(**user) for user in testdata.user]
            users_subscriptions = [
                UsersSubscriptions(**user_subscription)
                for user_subscription in testdata.users_subscriptions
            ]
            payment = [Payment(**payment) for payment in testdata.payment]
            subscription = [
                Subscription(
                    **subscription
                ) for subscription in testdata.subscription
            ]
            users_payment_method = [
                UsersPaymentMethods(**user_payment_method)
                for user_payment_method in testdata.users_payment_method
            ]
            payment_method = [
                PaymentMethod(**payment_method)
                for payment_method in testdata.payment_method
            ]

            session.add_all(users)
            session.add_all(users_subscriptions)
            session.add_all(payment)
            session.add_all(subscription)
            session.add_all(users_payment_method)
            session.add_all(payment_method)
            await session.commit()

    return inner


@pytest.fixture
def pg_write_data_only_user(pg_client):
    async def inner():
        async with pg_client.async_session() as session:
            subscription = [
                Subscription(
                    **subscription
                ) for subscription in testdata.subscription
            ]
            users = [User(**user) for user in testdata.user]
            session.add_all(users)
            session.add_all(subscription)
            await session.commit()

    return inner


@pytest.fixture
def pg_clear_data(pg_client):
    async def inner():
        await delete_all(pg_client)

    return inner
