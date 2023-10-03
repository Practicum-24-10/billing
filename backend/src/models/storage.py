from datetime import datetime
from uuid import UUID

from backend.src.models.model_mixin import OrjsonMixin


class SubscriptionModel(OrjsonMixin):
    id: UUID
    duration: int
    amount: float
    title: str
    currency: str


class AutoRenewalModel(OrjsonMixin):
    active: bool


class UserPaymentModel(OrjsonMixin):
    id: UUID
    created_at: datetime
    payment_status: str


class UserSubscriptionModel(OrjsonMixin):
    id: UUID
    start_at: datetime
    expires_at: datetime
    payments: list[UserPaymentModel]


class UserPaymentMethod(OrjsonMixin):
    id: UUID
    order: int
    card_type: str
    kassa_payment_method_id: str
    first_numbers: int
    last_numbers: int


class UserInfoModel(OrjsonMixin):
    id: UUID
    active: bool
    subscriptions: list[UserSubscriptionModel]
    payment_methods: list[UserPaymentMethod]
