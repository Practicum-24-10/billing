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
from backend.src.models.jwt import JWTPayload
from backend.src.models.kassa import DetailsPaymentModel, PaymentModel
from backend.src.services.mixin import MixinModel


class PaymentService(MixinModel):
    async def confirm_add_payment(self, redirect_uuid):
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

    async def add_payment_method(
        self, jwt: JWTPayload, payment_method: str, idempotence_key: UUID
    ):
        user_id = jwt.user_id
        redirect_uuid = uuid.uuid4()
        payment = PaymentModel(
            amount_value=1,
            amount_currency="RUB",
            payment_method=payment_method,
            redirect_url=f"http://localhost:8000/api/v1/payment/{str(redirect_uuid)}",
            save_payment=True,
        )
        details = DetailsPaymentModel(
            description="Привязка карты",
            metadata={"user_id": str(user_id), "cancel": True},
            idempotence_key=idempotence_key,
        )
        payment_link, payment_id = self._get_payment_link(payment, details)
        if payment_link:
            status = await self._add_data_to_cache(
                redirect_uuid, {"user_id": str(user_id), "payment_id": payment_id}
            )
            if status:
                return payment_link

    async def delete_payment_method(self, jwt: JWTPayload, payment_method_id: UUID):
        user_id = jwt.user_id
        return await self._delete_user_payment_method(user_id, payment_method_id)

    async def default_payment_method(self, jwt: JWTPayload, payment_method_id: UUID):
        user_id = jwt.user_id
        return await self._change_order_user_payment_method(user_id, payment_method_id)


@lru_cache()
def get_payment_service(
    kassa: AbstractKassa = Depends(get_yookassa),
    storage: AbstractStorage = Depends(get_postgres),
    cache: AbstractCache = Depends(get_redis),
) -> PaymentService:
    return PaymentService(kassa, storage, cache)
