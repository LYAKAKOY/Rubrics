import datetime
from typing import List

from api.base_schemas import TunedModel
from pydantic import BaseModel


class CreateRubrics(BaseModel):
    text: str
    rubrics: List[str]
    created_date: datetime.datetime


class ShowRubrics(TunedModel):
    id: int
    text: str
    rubrics: List[str]
    created_date: datetime.datetime


class DeleteRubrics(TunedModel):
    id: int
