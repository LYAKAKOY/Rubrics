import datetime
import json

import pytest

from tests.conftest import create_rubric


@pytest.mark.parametrize(
    "rubric_data, expected_status_code",
    [
        (
                {
                    "text": "Розыгрыш на кепки!",
                    "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                },
                200,
        ),
        (
                {
                    "text": "Розыгрыш на худи!",
                    "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                },
                200,
        ),
    ],
)
async def test_delete_rubric_handler(
        client,
        asyncpg_pool,
        test_async_client_es,
        rubric_data,
        expected_status_code,
):
    rubric_id = await create_rubric(asyncpg_pool=asyncpg_pool, rubric_id=10001,
                                    rubrics=rubric_data['rubrics'], text=rubric_data['text'],
                                    created_date=datetime.datetime.utcnow())

    response = await client.delete(
        f"/rubrics/{rubric_id}",
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("id") == rubric_id


async def test_delete_rubric_handler_not_found(
        client,
):
    response = await client.delete(
        "/rubrics/1242352",
    )
    data_from_response = response.json()
    assert response.status_code == 404
    assert data_from_response == {"detail": "the rubrics not found"}
