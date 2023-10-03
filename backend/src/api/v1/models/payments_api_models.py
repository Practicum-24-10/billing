from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentMethodEnum(str, Enum):
    bank_card = "bank_card"


class PaymentResponse(BaseModel):
    payment_link: str = Field(
        title="Ссылка на оплату", examples=["https://www.examples.com/return_url"]
    )


class PaymentDeleteResponse(BaseModel):
    status: bool = Field(title="Успех", examples=[True])


class PaymentModel(BaseModel):
    payment_method: PaymentMethodEnum = Field(
        title="payment_method", description="payment_method", examples=["bank_card"]
    )
    idempotence_key: UUID = Field(
        title="idempotence_key",
        description="idempotence_key",
        examples=["f39d7b6d-aef2-40b1-aaf0-cf05e7048011"],
    )


class PaymentDeletModel(BaseModel):
    payment_method_id: UUID = Field(
        title="payment_method_id",
        description="payment_method_id",
        examples=["d1bd3f2d-a97f-4a6b-99be-bd9f4c0680c0"],
    )


class PaymentAddResponse(BaseModel):
    status: bool = Field(title="Успех", examples=[True])
