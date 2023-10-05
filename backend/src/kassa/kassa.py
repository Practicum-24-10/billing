from abc import ABC
from http import HTTPStatus

from fastapi import HTTPException
from yookassa import Configuration, Payment
from yookassa.domain.exceptions import BadRequestError

from backend.src.local.api import errors
from backend.src.models.kassa import (
    DetailsPaymentModel,
    PaymentCard,
    PaymentModel,
    PaymentResponseModel,
)


class AbstractKassa(ABC):
    def get_new_payment(
            self, payment_params: PaymentModel, details: DetailsPaymentModel
    ) -> PaymentResponseModel | None:
        pass

    def confirm(self, payment_id: str):
        pass


class YooKassa(AbstractKassa):
    def __init__(self):
        Configuration.account_id = "255446"
        Configuration.secret_key = "test_6J9GVY4CgQmhyd74ZaucUjNC00eZ3USpMAfBQg5yrQk"
        self.payment = Payment()

    def confirm(self, payment_id: str):
        try:
            payment = self.payment.find_one(payment_id)
            if not payment:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=errors.YOOKASSA_PAYMENT_NOT_FOUND,
                )
            _ = self.payment.cancel(payment_id)
            if payment.status == "canceled":  # type: ignore
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=errors.YOOKASSA_PAYMENT_CANCELED,
                )
            if payment.status != "waiting_for_capture":  # type: ignore
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=errors.YOOKASSA_PAYMENT_NOT_WAITING_FOR_CAPTURE,
                )
            if not payment.payment_method.saved:  # type: ignore
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail=errors.YOOKASSA_PAYMENT_NOT_SAVE,
                )
            card = PaymentCard(
                card_type=payment.payment_method.card.card_type,  # type: ignore
                first6=payment.payment_method.card.first6,  # type: ignore
                last4=payment.payment_method.card.last4,  # type: ignore
            )

            return card
        except BadRequestError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))

    def get_new_payment(
            self, payment_params: PaymentModel, details: DetailsPaymentModel
    ) -> PaymentResponseModel | None:
        try:
            payment = self.payment.create(
                {
                    "amount": {
                        "value": payment_params.amount_value,
                        "currency": payment_params.amount_currency,
                    },
                    "payment_method_data": {"type": payment_params.payment_method},
                    "confirmation": {
                        "type": "redirect",
                        "return_url": payment_params.redirect_url,
                    },
                    "capture": False,
                    "description": details.description,
                    "save_payment_method": payment_params.save_payment,
                    "metadata": details.metadata,

                }, str(details.idempotence_key))
            if payment:
                return PaymentResponseModel(
                    id=payment.id,  # type: ignore
                    status=payment.status,  # type: ignore
                    payment_page=payment.confirmation.confirmation_url,  # type: ignore
                )
        except BadRequestError as e:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
