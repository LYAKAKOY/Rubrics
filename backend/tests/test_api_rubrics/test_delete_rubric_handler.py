import json

import pytest


@pytest.mark.parametrize(
    "rubric_date, expected_status_code",
    [
        (
            {
                "text": "Розыгрыш на кепки!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00",
            },
            200,
        ),
        (
            {
                "text": "Розыгрыш на худи!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00",
            },
            200,
        ),
    ],
)
async def test_delete_rubric_handler(
    client,
    rubric_date,
    expected_status_code,
):
    res = await client.post(
        "/rubrics/",
        content=json.dumps(rubric_date),
    )
    created_rubric = res.json()
    response = await client.delete(
        f"/rubrics/{created_rubric.get('id')}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("id") == created_rubric.get("id")


async def test_delete_rubric_handler_not_found(
    client,
):
    response = await client.delete(
        "/rubrics/1242352",
    )
    data_from_response = response.json()
    assert response.status_code == 404
    assert data_from_response == {"detail": "the rubrics not found"}
