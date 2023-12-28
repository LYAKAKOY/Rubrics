import datetime
from typing import List

import elastic_transport
import settings
from db.es.indexes import INDEX_RUBRICS
from db.pg.models import Rubric
from elasticsearch import AsyncElasticsearch
from sqlalchemy import Delete
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class RubricDAL:
    def __init__(self, pg_session: AsyncSession, es_session: AsyncElasticsearch):
        self.pg_session = pg_session
        self.es_session = es_session

    async def create_rubric(
        self, text: str, rubrics: List[str], created_date: datetime.datetime
    ) -> Rubric | None:
        new_rubrics = Rubric(text=text, rubrics=rubrics, created_date=created_date)
        try:
            self.pg_session.add(new_rubrics)
            await self.pg_session.flush()
            res_es = await self.es_session.index(
                index=INDEX_RUBRICS,
                document={"id": new_rubrics.id, "text": new_rubrics.text},
                refresh=True,
            )
            if res_es.meta.status != 201:
                await self.pg_session.rollback()
            await self.pg_session.commit()
            return new_rubrics
        except IntegrityError:
            await self.pg_session.rollback()
            return
        except elastic_transport.ConnectionError:
            await self.pg_session.rollback()
            return

    async def delete_rubric_by_id(self, id: int) -> int | None:
        query = Delete(Rubric).where(Rubric.id == id).returning(Rubric.id)
        try:
            deleted_id = await self.pg_session.scalar(query)
            res_es = await self.es_session.delete_by_query(
                index=INDEX_RUBRICS,
                query={"term": {"id": {"value": id}}},
                refresh=True,
            )
            if res_es.meta.status != 200:
                await self.pg_session.rollback()
            await self.pg_session.commit()
            return deleted_id
        except IntegrityError:
            await self.pg_session.rollback()
            return
        except elastic_transport.ConnectionError:
            await self.pg_session.rollback()
            return

    async def get_20_rubrics_by_text(self, text: str) -> List[Rubric] | None:
        res = await self.es_session.search(
            index=INDEX_RUBRICS,
            query={"match": {"text": {"query": text}}},
            size=20,
            scroll=settings.SCROLL_TIME,
        )
        rubrics_data = res.get("hits").get("hits")
        rubrics_ids = []
        scroll_id = res.get("_scroll_id")
        while rubrics_data:
            rubrics_ids.extend(
                [rubric.get("_source").get("id") for rubric in rubrics_data]
            )
            res = await self.es_session.options(ignore_status=400).scroll(
                scroll_id=scroll_id, scroll=settings.SCROLL_TIME
            )
            rubrics_data = res.get("hits").get("hits")

        if rubrics_ids:
            query = (
                Select(Rubric)
                .where(Rubric.id.in_(rubrics_ids))
                .order_by(Rubric.created_date)
                .limit(20)
            )
            rubrics = await self.pg_session.scalars(query)
            return rubrics
