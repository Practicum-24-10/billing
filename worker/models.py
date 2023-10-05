from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class CurrencyEnum(str, Enum):
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'
    CNY = 'CNY'
    INR = 'INR'
    KZT = 'KZT'
    UZS = 'UZS'
    GEL = 'GEL'
    ERN = 'ERN'
    AMD = 'AMD'
    AZN = 'AZN'
    TJS = 'TJS'


class ConfirmationEnum(str, Enum):
    REDIRECT = 'redirect'


class AmountModel(BaseModel):
    value: float
    currency: CurrencyEnum = CurrencyEnum.RUB


class ConfirmationModel(BaseModel):
    type: ConfirmationEnum = ConfirmationEnum.REDIRECT
    return_url: str


class RecipientModel(BaseModel):
    account_id: str
    gateway_id: str


class PaymentModel(BaseModel):
    amount: AmountModel
    capture: bool = True
    confirmation: ConfirmationModel
    created_at: datetime = Field(default_factory=datetime.now)
    description: str = ''
    metadata: dict = {}
    recipient: RecipientModel
    refundable: bool = False
    test: bool = True


class AutopaymentModel(BaseModel):
    amount: AmountModel
    capture: bool
    payment_method_id: UUID
    description: str


class UserSubscriptionCreateModel(BaseModel):
    user_id: UUID
    subscription_id: UUID
    amount: AmountModel
    plan: str
