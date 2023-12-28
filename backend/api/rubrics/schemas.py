import datetime
from typing import List

from api.base_schemas import TunedModel
from pydantic import BaseModel


class CreateRubric(BaseModel):
    text: str
    rubrics: List[str] = []
    created_date: datetime.datetime = datetime.datetime.utcnow()


class ShowRubric(TunedModel):
    id: int
    text: str
    rubrics: List[str]
    created_date: datetime.datetime


class DeletedRubric(TunedModel):
    id: int
