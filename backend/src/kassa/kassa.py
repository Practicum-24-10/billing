from abc import ABC
from http import HTTPStatus
from uuid import UUID

from fastapi import HTTPException
from yookassa import Configuration, Payment
from yookassa.domain.exceptions import BadRequestError

from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentModel,
    PaymentResponseModel, PaymentCard,
)


class AbstractKassa(ABC):
    def get_new_payment(self, payment_params: PaymentModel,
                        details: DetailsPaymentModel) -> PaymentResponseModel:
        pass

    def confirm(self, payment_id: str):
        pass


class YooKassa(AbstractKassa):
    def __init__(self):
        Configuration.account_id = "255446"
        Configuration.secret_key = "test_6J9GVY4CgQmhyd74ZaucUjNC00eZ3USpMAfBQg5yrQk"
        self.payment = Payment()

    def confirm(self, payment_id: str):
        payment = self.payment.find_one(payment_id)
        if not payment or payment.status != "waiting_for_capture" or not payment.payment_method.saved:
            return None
        card = PaymentCard(card_type=payment.payment_method.card.card_type,
                           first6=payment.payment_method.card.first6,
                           last4=payment.payment_method.card.last4)
        status = self.payment.cancel(payment_id)


        return card

    def get_new_payment(self, payment_params: PaymentModel,
                        details: DetailsPaymentModel) -> PaymentResponseModel | str:
        try:
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
                "save_payment_method": payment_params.save_payment,
                "metadata": details.metadata
            })
            # }, str(details.idempotence_key))
            return PaymentResponseModel(id=payment.id, status=payment.status,
                                        payment_page=payment.confirmation.confirmation_url)
        except BadRequestError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=str(e))

        # except BadRequestError as e:
        #     raise HTTPException(
        #         status_code=e.HTTP_CODE,
        #         detail=e.args[0]['description'])
        # return BadRequestErrore.args[0]['description']
