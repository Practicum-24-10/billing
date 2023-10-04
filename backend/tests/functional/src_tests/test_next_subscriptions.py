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
                    "subscription_id":
                        "94791a79-42a0-46cc-b231-9d8f61569b47"
                },
            },
            {
                "status": HTTPStatus.OK,
            },
        )
    ],
)
@pytestmark
async def test_next_subscription(
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
    url = "subscription/change_next_subscription"
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


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"jwt": testdata.jwt, "body": {
                "subscription_id": ""
            }
             },
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {
                "jwt": testdata.jwt,
                "body": {
                    "subscription_id":
                        "b087df75-afff-43c3-9827-1903ea7d1baa"
                },
            },
            {
                "status": HTTPStatus.BAD_REQUEST,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": ""},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt,
             "body": {
                "subscription_id": 1111
             }
             },
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
    ],
)
@pytestmark
async def test_next_subscription_bad(
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
    url = "subscription/change_next_subscription"
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
