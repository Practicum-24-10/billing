from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class CurrencyEnum(str, Enum):
    RUB = 'RUB'
    USD = 'USD'


class ConfirmationEnum(str, Enum):
    REDIRECT = 'redirect'


class AmountModel(BaseModel):
    value: Decimal = Field(decimal_places=2)
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
