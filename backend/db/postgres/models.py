import datetime
from typing import List
from sqlalchemy import String, DateTime, ARRAY
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from db.base import Base


class Rubric(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True
    )
    rubrics: Mapped[List[str]] = mapped_column(ARRAY(String))
    text: Mapped[str]
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    def model_to_dict(self):
        return {"id": self.id, "text": self.text}
