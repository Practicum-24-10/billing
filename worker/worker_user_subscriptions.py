import asyncio

from message_broker.amqp import tasks_master
from worker.tasks import create_user_subscription


async def main() -> None:
    async with tasks_master() as master:
        await master.create_worker('create_user_subscription',
                                   create_user_subscription,
                                   auto_delete=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
