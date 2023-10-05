from http import HTTPStatus

import pytest

from backend.tests.functional import testdata

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    "expected_answer",
    [
        ({"status": HTTPStatus.OK, "subscriptions": testdata.subscription}),
    ],
)
@pytestmark
async def test_sub_all(
        pg_write_data,
        pg_clear_data,
        make_get_request,
        make_post_request,
        expected_answer
):
    # Arrange
    await pg_clear_data()
    await pg_write_data()
    url = "subscription/all"
    # Act
    response = await make_get_request(url)
    # Assert
    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == len(expected_answer["subscriptions"])
