from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from backend.src.local.api import errors
from backend.src.models.jwt import JWTPayload
from backend.src.services.autorization import get_token_payload
from backend.src.services.payments import PaymentService, get_payment_service

from .models.payments_api_models import *

router = APIRouter()


@router.post(
    "/add_payment_method",
    response_description="Add Payment",
    response_model=PaymentResponse,
    summary="Добавление метода оплаты",
)
async def add_payment_method(
    body: PaymentModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    payments_service: PaymentService = Depends(get_payment_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    payment_link = await payments_service.add_payment_method(
        jwt, body.payment_method, body.idempotence_key
    )
    if payment_link:
        return PaymentResponse(payment_link=payment_link)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED)


@router.post(
    "/delete_payment_method",
    response_description="Delete Payment",
    response_model=PaymentDeleteResponse,
    summary="Удаление метода оплаты",
)
async def delete_payment_method(
    body: PaymentDeletModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    payments_service: PaymentService = Depends(get_payment_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    result = await payments_service.delete_payment_method(jwt, body.payment_method_id)
    if result:
        return PaymentDeleteResponse(status=True)
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=errors.POSTGRES_USER_METHODE_ID_NOT_FOUND,
    )


@router.post(
    "/default_payment_method",
    response_description="Delete Payment",
    response_model=PaymentDeleteResponse,
    summary="Установка метода оплаты по умолчанию",
)
async def default_payment_method(
    body: PaymentDeletModel,
    jwt: None | JWTPayload = Depends(get_token_payload),
    payments_service: PaymentService = Depends(get_payment_service),
):
    if jwt is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail=errors.NO_AUTHORIZED
        )
    result = await payments_service.default_payment_method(jwt, body.payment_method_id)
    if result:
        return PaymentDeleteResponse(status=True)
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=errors.POSTGRES_USER_METHODE_ID_NOT_FOUND,
    )


@router.get(
    "/{redirect_uuid}",
    response_description="Страница редиректа",
    response_model=PaymentAddResponse,
    summary="Редирект для подтверждения добавления метода оплаты",
)
async def redirect(
    redirect_uuid: Annotated[
        UUID,
        Path(
            description="redirect_uuid", example="77bff1a8-f6e2-4a6c-b555-b5d44c34c0dd"
        ),
    ],
    payments_service: PaymentService = Depends(get_payment_service),
):
    status = await payments_service.confirm_add_payment(redirect_uuid)
    if status:
        return PaymentAddResponse(status=True)
    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=errors.NO_AUTHORIZED)
