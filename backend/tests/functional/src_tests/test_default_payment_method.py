from http import HTTPStatus

import pytest

from backend.tests.functional import testdata

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id":
                        testdata.users_payment_method[0]["id"],
                },
            },
            {
                "status": HTTPStatus.OK,
                "payment_method_id": testdata.users_payment_method[0]["id"],
                "order": 2,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id":
                        testdata.users_payment_method[1]["id"],
                },
            },
            {
                "status": HTTPStatus.OK,
                "payment_method_id":
                    testdata.users_payment_method[1]["id"],
                "order": 2,
            },
        ),
    ],
)
@pytestmark
async def test_default_payment_method(
    pg_write_data,
    pg_clear_data,
    make_get_request,
    make_post_request,
    query_data,
    expected_answer,
):
    # Arrange
    await pg_clear_data()
    await pg_write_data()
    url = "payment/default_payment_method"
    url_2 = "subscription/user_info"
    access_token = query_data["jwt"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Act
    response = await make_post_request(
        url,
        params=query_data["body"],
        headers=headers
    )
    response_2 = await make_get_request(url_2, headers=headers)
    # Assert
    assert response["status"] == expected_answer["status"]
    assert response_2["status"] == expected_answer["status"]
    for methods in response_2["body"]["payment_methods"]:
        if methods["id"] == expected_answer["payment_method_id"]:
            assert methods["order"] == expected_answer["order"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id": "",
                },
            },
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id": 11,
                },
            },
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id": "4343",
                },
            },
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": ""},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "payment_method_id":
                        "92336d84-e39d-4c43-a40b-565821551b21",
                },
            },
            {
                "status": HTTPStatus.NOT_FOUND,
            },
        ),
    ],
)
@pytestmark
async def test_default_payment_method_bad(
    pg_write_data,
    pg_clear_data,
    make_get_request,
    make_post_request,
    query_data,
    expected_answer,
):
    # Arrange
    await pg_clear_data()
    await pg_write_data()
    url = "payment/default_payment_method"
    access_token = query_data["jwt"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Act
    response = await make_post_request(
        url,
        params=query_data["body"],
        headers=headers
    )
    # Assert
    assert response["status"] == expected_answer["status"]
