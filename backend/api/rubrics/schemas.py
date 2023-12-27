import datetime
from typing import List

from api.base_schemas import TunedModel
from pydantic import BaseModel


class CreateRubric(BaseModel):
    text: str
    rubrics: List[str]
    created_date: datetime.datetime


class ShowRubric(TunedModel):
    id: int
    text: str
    rubrics: List[str]
    created_date: datetime.datetime


class DeleteRubric(TunedModel):
    id: int
