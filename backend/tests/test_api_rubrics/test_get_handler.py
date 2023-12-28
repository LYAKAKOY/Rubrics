from copy import deepcopy
from datetime import datetime

import pytest
from tests.conftest import create_rubric


@pytest.mark.parametrize(
    "rubric_data, count, text, expected_count, expected_status_code",
    [
        (
            {
                "text": "Розыгрыш на пиццу!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00Z",
            },
            30,
            "Розыгрыш",
            20,
            200,
        ),
        (
            {
                "text": "Розыгрыш на пиццу!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00Z",
            },
            5,
            "пиццу",
            5,
            200,
        ),
        (
            {
                "text": "Розыгрыш на пиццу!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00Z",
            },
            5,
            "Худи",
            0,
            200,
        ),
    ],
)
async def test_get_20_rubrics_handler(
    client,
    asyncpg_pool,
    rubric_data,
    count,
    text,
    expected_count,
    expected_status_code,
):
    all_rubrics = []
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    for minute in range(10, count + 10):
        rubric_data["created_date"] = f"2023-12-26T09:{minute}:00Z"
        await create_rubric(
            asyncpg_pool=asyncpg_pool,
            rubric_id=minute,
            rubrics=rubric_data["rubrics"],
            text=rubric_data["text"],
            created_date=datetime.strptime(rubric_data["created_date"], date_format),
        )
        all_rubrics.append(deepcopy(rubric_data))
    for i in range(9):
        await create_rubric(
            asyncpg_pool=asyncpg_pool,
            rubric_id=i,
            rubrics=["vk/6, vk/8"],
            text="Раздача призов",
            created_date=datetime.strptime(f"200{i}-12-26T09:50:00Z", date_format),
        )
    response = await client.get(
        f"/rubrics/{text}",
    )
    data_from_response = response.json()
    if expected_count:
        assert len(data_from_response) == expected_count
    for data_res, rubric in zip(data_from_response, all_rubrics[:expected_count]):
        assert data_res.get("text") == rubric.get("text")
        assert data_res.get("rubrics") == rubric.get("rubrics")
        assert data_res.get("created_date") == rubric.get("created_date")


async def test_get_20_rubrics_handler_not_found(
    client,
):
    response = await client.get(
        "/rubrics/Розыгрыш",
    )
    data_from_response = response.json()
    assert response.status_code == 404
    assert data_from_response == {"detail": "the rubrics not found"}
