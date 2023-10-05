import uuid
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
                    "payment_method": "bank_card",
                    "idempotence_key": str(uuid.uuid4()),
                },
            },
            {"status_1": HTTPStatus.OK, "status_2": HTTPStatus.BAD_REQUEST},
        )
    ],
)
@pytestmark
async def test_add_payment_method(
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
    url = "payment/add_payment_method"
    access_token = query_data["jwt"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    # Act
    response_1 = await make_post_request(
        url, params=query_data["body"], headers=headers
    )
    response_2 = await make_post_request(
        url, params=query_data["body"], headers=headers
    )
    # Assert
    assert response_1["status"] == expected_answer["status_1"]
    assert response_2["status"] == expected_answer["status_2"]
