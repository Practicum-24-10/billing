from abc import ABC
from uuid import UUID

from fastapi import HTTPException
from yookassa import Configuration, Payment
from yookassa.domain.exceptions import BadRequestError

from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentModel,
    PaymentResponseModel,
)


class AbstractKassa(ABC):
    def get_new_payment(self, user_id: UUID, payment_params: PaymentModel,
                        details: DetailsPaymentModel) -> PaymentResponseModel:
        pass


class YooKassa(AbstractKassa):
    def __init__(self):
        Configuration.account_id = "255446"
        Configuration.secret_key = "test_6J9GVY4CgQmhyd74ZaucUjNC00eZ3USpMAfBQg5yrQk"
        self.payment = Payment()

    def get_new_payment(self, user_id: UUID, payment_params: PaymentModel,
                        details: DetailsPaymentModel) -> PaymentResponseModel | str:
        # try:

        payment = self.payment.create({
            "amount": {
                "value": payment_params.amount_value,
                "currency": payment_params.amount_currency
            },
            "payment_method_data": {
                "type": payment_params.payment_method
            },
            "confirmation": {
                "type": "redirect",
                "return_url": payment_params.redirect_url
            },
            "capture": False,
            "description": details.description,
            "save_payment_method": True,
            "metadata": {
                "user_id": str(user_id)
            }
        }, str(details.idempotence_key))
        return PaymentResponseModel(id=payment.id, status=payment.status,
                                    payment_page=payment.confirmation.confirmation_url)
        # except BadRequestError as e:
        #     raise HTTPException(
        #         status_code=e.HTTP_CODE,
        #         detail=e.args[0]['description'])
            # return BadRequestErrore.args[0]['description']
