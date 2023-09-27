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
from backend.src.db import postgres
from backend.src.db.storage import PostgresStorage
from backend.src.kassa import yoo_kassa
from backend.src.kassa.kassa import YooKassa

if config.logging_on:
    sentry_sdk.init(dsn=config.sentry_dsn, integrations=[FastApiIntegration()])

    logging.basicConfig(**LOGGING)
    log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    rsa_key.pk = RsaKey(path=PUBLIC_KEY, algorithms=["RS256"])
    yoo_kassa.yk = YooKassa()
    postgres.pg = PostgresStorage()
    yield


app = FastAPI(
    title=config.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(subscription_router, prefix="/api/v1/subscription", tags=["subscription"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8004, reload=True)
