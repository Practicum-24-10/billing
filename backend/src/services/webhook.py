import asyncio
import uuid
from functools import lru_cache
from uuid import UUID

from fastapi import Depends

from backend.src.db.cache import AbstractCache
from backend.src.db.postgres import get_postgres
from backend.src.db.redis_db import get_redis
from backend.src.db.storage import AbstractStorage
from backend.src.kassa.kassa import AbstractKassa
from backend.src.kassa.yoo_kassa import get_yookassa
from backend.src.services.mixin import MixinModel


class WebhookService(MixinModel):
    async def confirm_webhook(self, data):
        redirect_uuid = data["metadata"].get("redirect_uuid")
        if redirect_uuid:
            return await self.confirm_add_payment_method(data["paymentStatus"],
                                                         uuid.UUID(redirect_uuid))

    async def confirm_payment(self):
        pass

    async def confirm_add_payment_method(self, status: str, redirect_uuid: UUID):
        if status == "waiting_for_capture":
            await asyncio.sleep(5)
            data = await self._get_data_from_cache(redirect_uuid)
            if not data:
                return False
            card = self._check_conformation_payment(data["payment_id"])
            if not card:
                return False
            result = await self._check_and_add_new_card(
                card, data["user_id"], data["payment_id"]
            )
            if not result:
                return False
            return True
        else:
            return True


@lru_cache()
def get_webhook_service(
        kassa: AbstractKassa = Depends(get_yookassa),
        storage: AbstractStorage = Depends(get_postgres),
        cache: AbstractCache = Depends(get_redis),
) -> WebhookService:
    return WebhookService(kassa, storage, cache)
