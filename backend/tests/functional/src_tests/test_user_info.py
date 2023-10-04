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
            },
            {
                "status": HTTPStatus.OK,
                "user": testdata.user[0],
                "users_payment_method": testdata.users_payment_method,
                "subscriptions": testdata.users_subscriptions,
            },
        ),
    ],
)
@pytestmark
async def test_user_info(
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
    url = "subscription/user_info"
    access_token = query_data["jwt"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_get_request(url, headers=headers)
    # Assert
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]["payment_methods"]) == len(
        expected_answer["users_payment_method"]
    )
    assert len(response["body"]["subscriptions"]) == len(
        expected_answer["users_payment_method"]
    )


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {
                "jwt": "",
            },
            {"status": HTTPStatus.UNAUTHORIZED, "detail": "no authorized"},
        ),
    ],
)
@pytestmark
async def test_user_info_no_jwt(
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
    url = "subscription/user_info"
    access_token = query_data["jwt"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    # Act
    response = await make_get_request(url, headers=headers)
    # Assert
    assert response["status"] == expected_answer["status"]
    assert response["body"]["detail"] == expected_answer["detail"]
