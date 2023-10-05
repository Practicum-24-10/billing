from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class PaymentMethodEnum(str, Enum):
    bank_card = "bank_card"


class SubscriptionsResponse(BaseModel):
    id: UUID = Field(title="id", examples=["4791a79-42a0-46cc-b231-9d8f61569b47"])
    duration: int = Field(title="Продолжительность", examples=[30])
    price: float = Field(title="Стоимость", examples=[300])
    title: str = Field(title="Название подписки", examples=["HD"])
    currency: str = Field(title="Валюта", examples=["RUB"])


class NewSubscriptionModel(BaseModel):
    subscription_id: UUID = Field(
        title="subscription_id",
        description="subscription_id",
        examples=["94791a79-42a0-46cc-b231-9d8f61569b47"],
    )


class NewSubscriptionResponse(BaseModel):
    status: bool = Field(title="Успех", examples=[True])


class UserPaymentResponse(BaseModel):
    id: UUID = Field(
        title="ID оплаты за подписку", examples=["f39d7b6d-aef2-40b1-aaf0-cf05e7048011"]
    )
    created_at: datetime = Field(
        title="Дата создания платежа", examples=[datetime.now()]
    )
    payment_status: str = Field(title="Статус платежа", examples=["succeeded"])


class UserSubscriptionResponse(BaseModel):
    id: UUID = Field(
        title="ID подписки пользователя",
        examples=["f39d7b6d-aef2-40b1-aaf0-cf05e7048011"],
    )
    start_at: datetime = Field(title="Время начала подписки", examples=[datetime.now()])
    expires_at: datetime = Field(
        title="Время окончания подписки", examples=[datetime.now()]
    )
    payments: list[UserPaymentResponse] = Field(title="Оплаты подписки")


class UserPaymentMethodResponse(BaseModel):
    id: UUID = Field(
        title="ID метода оплаты пользователя",
        examples=["f39d7b6d-aef2-40b1-aaf0-cf05e7048011"],
    )
    order: int = Field(title="Очердь метода оплаты", examples=[0])
    card_type: str = Field(title="Очердь метода оплаты", examples=["MasterCard"])
    first_numbers: int = Field(title="Первые 6 цифр карты", examples=[555555])
    last_numbers: int = Field(title="Последние 4 цифры карты", examples=[4444])


class UserInfoResponse(BaseModel):
    id: UUID = Field(
        title="ID пользователя", examples=["94791a79-42a0-46cc-b231-9d8f61569b47"]
    )
    active: bool = Field(title="Автопродление", examples=[True])
    subscriptions: list[UserSubscriptionResponse] = Field(title="Подписки")
    payment_methods: list[UserPaymentMethodResponse] = Field(title="Методы оплаты")


class CancelSubModel(BaseModel):
    time: int = Field(
        title="unix timestamp",
        description="Время",
        examples=[1611039931],
        gt=0,
        lt=9999999999,
    )


class CancelSubResponse(BaseModel):
    status: bool = Field(title="Успех", examples=[True])


class AutoRenewalModel(BaseModel):
    active: bool = Field(title="Новый статус продления подписки", examples=[True])


class NextSubModel(BaseModel):
    subscription_id: UUID = Field(
        title="subscription_id",
        description="subscription_id",
        examples=["94791a79-42a0-46cc-b231-9d8f61569b47"],
    )


class NextSubResponse(BaseModel):
    status: bool = Field(title="Успех", examples=[True])


class AutoRenewalResponse(BaseModel):
    active: bool = Field(title="Новый статус продления подписки", examples=[True])
