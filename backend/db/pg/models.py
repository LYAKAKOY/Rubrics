import datetime
from typing import List

from db.base import Base
from sqlalchemy import ARRAY
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Rubric(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    rubrics: Mapped[List[str]] = mapped_column(ARRAY(String))
    text: Mapped[str]
    created_date: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    def model_to_dict(self):
        return {"id": self.id, "text": self.text}
