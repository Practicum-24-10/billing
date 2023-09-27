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
        self.async_session: async_sessionmaker[AsyncSession] | None = None
        self._engine: AsyncEngine | None = None

    async def start(self):
        self._engine = create_async_engine(self.url)
        self.async_session = async_sessionmaker(
            bind=self._engine, expire_on_commit=False
        )

    async def close(self):
        if self._engine:
            await self._engine.dispose()
