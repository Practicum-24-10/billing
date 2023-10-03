from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class CurrencyEnum(str, Enum):
    RUB = 'RUB'
    USD = 'USD'


class ConfirmationEnum(str, Enum):
    REDIRECT = 'redirect'


class AmountModel(BaseModel):
    value: int = 0
    currency: CurrencyEnum = CurrencyEnum.RUB


class ConfirmationModel(BaseModel):
    type: ConfirmationEnum
    return_url: str


class RecipientModel(BaseModel):
    account_id: str
    gateway_id: str


class PaymentModel(BaseModel):
    amount: AmountModel
    capture: bool = True
    confirmation: ConfirmationModel
    created_at: datetime
    description: str = ''
    metadata: dict
    refundable: bool = False
    test: bool = True
