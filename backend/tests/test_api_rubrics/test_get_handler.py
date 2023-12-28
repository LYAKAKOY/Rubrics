import json
from copy import deepcopy
import pytest


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
        rubric_data,
        count,
        text,
        expected_count,
        expected_status_code,
):
    all_rubrics = []
    for minute in range(10, count+10):
        rubric_data["created_date"] = f"2023-12-26T09:{minute}:00Z"
        await client.post(
            "/rubrics/",
            content=json.dumps(rubric_data),
        )
        all_rubrics.append(deepcopy(rubric_data))
    response = await client.get(
        f"/rubrics/{text}",
    )
    data_from_response = response.json()
    assert len(data_from_response) <= 1
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