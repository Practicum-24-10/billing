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
                "body": {"subscription_id": testdata.subscription[0]["id"]},
            },
            {
                "status": HTTPStatus.OK,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {"subscription_id": testdata.subscription[1]["id"]},
            },
            {
                "status": HTTPStatus.OK,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {"subscription_id": testdata.subscription[2]["id"]},
            },
            {
                "status": HTTPStatus.OK,
            },
        ),
    ],
)
@pytestmark
async def test_pay_new_subscription(
    pg_write_data_only_user,
    pg_clear_data,
    make_get_request,
    make_post_request,
    query_data,
    expected_answer,
):
    # Arrange
    await pg_clear_data()
    await pg_write_data_only_user()
    url = "subscription/pay_new_subscription"
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
    await pg_clear_data()
    # Assert
    assert response["status"] == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "jwt": testdata.jwt,
                "body": {"subscription_id": testdata.subscription[0]["id"]},
            },
            {
                "status": HTTPStatus.BAD_REQUEST,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {"subscription_id": testdata.subscription[1]["id"]},
            },
            {
                "status": HTTPStatus.BAD_REQUEST,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {"subscription_id": testdata.subscription[2]["id"]},
            },
            {
                "status": HTTPStatus.BAD_REQUEST,
            },
        ),
    ],
)
@pytestmark
async def test_pay_new_subscription_bad(
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
    url = "subscription/pay_new_subscription"
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
    await pg_clear_data()
    # Assert
    assert response["status"] == expected_answer["status"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"jwt": testdata.jwt, "body": {"subscription_id": ""}},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": {"subscription_id": 12212}},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": {"subscription_id": "123232"}},
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
                    "subscription_id":
                        "6f6e6052-b23d-4149-98a1-c59a6a8c96a7"
                },
            },
            {
                "status": HTTPStatus.BAD_REQUEST,
            },
        ),
    ],
)
@pytestmark
async def test_pay_new_subscription_bad_request(
    pg_write_data_only_user,
    pg_clear_data,
    make_get_request,
    make_post_request,
    query_data,
    expected_answer,
):
    # Arrange
    await pg_clear_data()
    await pg_write_data_only_user()
    url = "subscription/pay_new_subscription"
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
