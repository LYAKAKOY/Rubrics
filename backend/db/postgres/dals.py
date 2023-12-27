import datetime
from typing import List
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from db.postgres.models import Rubric
from sqlalchemy import Delete


class RubricDAL:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_rubric(self, text: str, rubrics: List[str], created_date: datetime.datetime) -> Rubric | None:
        new_rubrics = Rubric(text=text, rubrics=rubrics, created_date=created_date)
        try:
            self.db_session.add(new_rubrics)
            await self.db_session.flush()
            await self.db_session.commit()
            return new_rubrics
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def delete_rubric_by_id(self, id: int):
        query = Delete(Rubric).where(Rubric.id == id).returning(Rubric.id)
        try:
            deleted_id = await self.db_session.scalar(query)
            await self.db_session.commit()
            return deleted_id
        except IntegrityError:
            await self.db_session.rollback()
            return

    async def get_rubric_by_id(self, id: int):
        rubrics = await self.db_session.get(Rubric, id)
        if rubrics is not None:
            return rubrics
