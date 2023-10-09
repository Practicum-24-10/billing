from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from admin.config import pg_config

engine = create_async_engine(
    "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
        pg_config.db_user,
        pg_config.db_password,
        pg_config.db_host,
        pg_config.db_port,
        pg_config.db_name,
    ),
    echo=True,
)

async_session = async_sessionmaker(engine)
