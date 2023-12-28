import json

import pytest


@pytest.mark.parametrize(
    "rubric_data, expected_status_code",
    [
        (
            {
                "text": "Розыгрыш на пиццу!",
                "rubrics": ["vk.com/1", "vk.com/2", "vk.com/3"],
                "created_date": "2019-12-26T09:27:00",
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
        (
            {
                "text": "Розыгрыш на пиццу!",
                "created_date": "2019-12-26T09:27:00",
            },
            200,
        ),
    ],
)
async def test_create_rubric_handler(
    client,
    rubric_data,
    expected_status_code,
):
    response = await client.post(
        "/rubrics/",
        content=json.dumps(rubric_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response.get("text") == rubric_data.get("text")
    if rubric_data.get("rubrics"):
        assert data_from_response.get("rubrics") == rubric_data.get("rubrics")
    else:
        assert data_from_response.get("rubrics") == []
    if rubric_data.get("created_date"):
        assert data_from_response.get("created_date") == rubric_data.get("created_date")


@pytest.mark.parametrize(
    "rubric_data, expected_data, expected_status_code",
    [
        (
            {},
            {
                "detail": [
                    {
                        "input": {},
                        "loc": ["body", "text"],
                        "msg": "Field required",
                        "type": "missing",
                        "url": "https://errors.pydantic.dev/2.5/v/missing",
                    }
                ]
            },
            422,
        )
    ],
)
async def test_create_rubric_handler_exceptions(
    client,
    rubric_data,
    expected_data,
    expected_status_code,
):
    response = await client.post(
        "/rubrics/",
        content=json.dumps(rubric_data),
    )
    data_from_response = response.json()
    assert response.status_code == expected_status_code
    assert data_from_response == expected_data
