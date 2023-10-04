from http import HTTPStatus

import pytest

from backend.tests.functional import testdata

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"jwt": testdata.jwt, "body": {"active": True}},
            {"status": HTTPStatus.OK, "active": True},
        ),
        (
            {"jwt": testdata.jwt, "body": {"active": False}},
            {"status": HTTPStatus.OK, "active": False},
        ),
    ],
)
@pytestmark
async def test_auto_renevall(
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
    url = "subscription/auto_renewal"
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
    assert response_2["body"]["active"] == expected_answer["active"]


@pytest.mark.parametrize(
    "query_data, expected_answer",
    [
        (
            {"jwt": testdata.jwt, "body": {"active": ""}},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": {"active": 312312}},
            {
                "status": HTTPStatus.UNPROCESSABLE_ENTITY,
            },
        ),
        (
            {"jwt": testdata.jwt, "body": {"active": "werwerwe"}},
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
    ],
)
@pytestmark
async def test_auto_renevall_bad(
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
    url = "subscription/auto_renewal"
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
