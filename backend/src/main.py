import logging
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from backend.src.api.v1.subscriptions_api import router as subscription_router
from backend.src.auth import rsa_key
from backend.src.auth.abc_key import RsaKey
from backend.src.core.config import PUBLIC_KEY, config
from backend.src.core.logger import LOGGING
from backend.src.db import postgres, redis_db
from backend.src.db.cache import RedisCache
from backend.src.db.storage import PostgresStorage
from backend.src.kassa import yoo_kassa
from backend.src.kassa.kassa import YooKassa
from database.core import pg_config

if config.logging_on:
    sentry_sdk.init(dsn=config.sentry_dsn, integrations=[FastApiIntegration()])

    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_db.redis = RedisCache(host=config.redis_host, port=config.redis_port,
                                expire=6000)
    rsa_key.pk = RsaKey(path=PUBLIC_KEY, algorithms=["RS256"])
    yoo_kassa.yk = YooKassa()
    postgres.pg = PostgresStorage(pg_config.db_user,
                                  pg_config.db_password,
                                  pg_config.db_host,
                                  pg_config.db_port,
                                  pg_config.db_name)
    await postgres.pg.start()
    yield
    await postgres.pg.end()
    await redis_db.redis.close()


app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

app.include_router(subscription_router, prefix="/api/v1/subscription",
                   tags=["subscription"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
