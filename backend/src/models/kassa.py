from uuid import UUID

from backend.src.models.model_mixin import OrjsonMixin


class PaymentModel(OrjsonMixin):
    amount_value: float
    amount_currency: str
    payment_method: str
    redirect_url: str
    save_payment: bool


class PaymentResponseModel(OrjsonMixin):
    id: str
    status: str
    payment_page: str


class PaymentCard(OrjsonMixin):
    card_type: str
    first6: int | None
    last4: int


class DetailsPaymentModel(OrjsonMixin):
    description: str
    metadata: dict
    idempotence_key: UUID


# class BadRequestError(OrjsonMixin):
#     di


class SubscriptionModel(OrjsonMixin):
    id: UUID
    price: float
    currency: str
    title: str
    duration: int
