from typing import List

from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession

import settings
from api.rubrics.schemas import CreateRubric, ShowRubric, DeletedRubric
from db.elasticsearch.indexes import INDEX_RUBRICS
from db.postgres.dals import RubricDAL
from db.rabbitmq.sender import set_task


async def _create_rubric(rubric: CreateRubric, pg_session: AsyncSession) -> ShowRubric | None:
    async with pg_session.begin():
        rubric_dal = RubricDAL(pg_session)
        res_pg = await rubric_dal.create_rubric(text=rubric.text, rubrics=rubric.rubrics,
                                                created_date=rubric.created_date)
        if res_pg is None:
            return

    await set_task(settings.RABBIT_QUEUE_CREATE_TASK, id=res_pg.id, text=res_pg.text)

    return ShowRubric(id=res_pg.id, text=res_pg.text, rubrics=res_pg.rubrics, created_date=res_pg.created_date)


async def _get_all_rubrics_by_text(text: str, pg_session: AsyncSession, es_session: AsyncElasticsearch) -> List[
                                                                                                               ShowRubric] | None:
    res = await es_session.search(
        index=INDEX_RUBRICS,
        query={"match": {"text": {"query": text}}},
        size=20
    )
    rubrics_data = res.get("hits").get("hits")
    if rubrics_data:
        id_rubrics = [
            rubric.get("_source").get("id")
            for rubric in rubrics_data
        ]
        rubric_dal = RubricDAL(pg_session)
        all_rubrics = sorted([await rubric_dal.get_rubric_by_id(id) for id in id_rubrics],
                             key=lambda rubric: rubric.created_date)
        return [ShowRubric(id=rubric.id, text=rubric.text, rubrics=rubric.rubrics, created_date=rubric.created_date)
                for rubric in all_rubrics]


async def _delete_rubric_by_id(id: int, pg_session: AsyncSession) -> DeletedRubric | None:

    async with pg_session.begin():
        rubric_dal = RubricDAL(pg_session)
        deleted_id = await rubric_dal.delete_rubric_by_id(id=id)
        if deleted_id is None:
            return
    await set_task(settings.RABBIT_QUEUE_DELETE_TASK, id=id)
    return DeletedRubric(id=deleted_id)
