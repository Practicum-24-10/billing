import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from aio_pika import connect_robust
from aio_pika.abc import AbstractChannel
from aio_pika.patterns import Master

from message_broker.settings import settings


async def get_channel() -> AsyncGenerator[AbstractChannel, None]:
    connection = await connect_robust(settings.get_amqp_url())
    async with connection:
        yield await connection.channel()


@asynccontextmanager
async def tasks_master() -> AsyncGenerator[Master, None]:
    connection = await connect_robust(settings.get_amqp_url())
    channel = await connection.channel()
    yield Master(channel)
    try:
        await asyncio.Future()
    finally:
        await connection.close()
