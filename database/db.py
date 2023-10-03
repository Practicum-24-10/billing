from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class AsyncPostgres:
    def __init__(self, user, password, host, port, name):
        self.url = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            user,
            password,
            host,
            port,
            name,
        )
        self.engine: AsyncEngine = create_async_engine(self.url)
        self.async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )

    async def close(self):
        if self.engine:
            await self.engine.dispose()
