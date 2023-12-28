from typing import List
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession
from api.rubrics.schemas import CreateRubric, ShowRubric, DeletedRubric
from db.dals import RubricDAL


async def _create_rubric(rubric: CreateRubric, pg_session: AsyncSession,
                         es_session: AsyncElasticsearch) -> ShowRubric | None:
    async with pg_session.begin():
        rubric_dal = RubricDAL(pg_session, es_session)
        new_rubric = await rubric_dal.create_rubric(text=rubric.text, rubrics=rubric.rubrics,
                                                    created_date=rubric.created_date)
        if new_rubric is None:
            return

    return ShowRubric(id=new_rubric.id, text=new_rubric.text, rubrics=new_rubric.rubrics,
                      created_date=new_rubric.created_date)


async def _get_20_rubrics_by_text(text: str, pg_session: AsyncSession, es_session: AsyncElasticsearch) -> List[
                                                                                                               ShowRubric] | None:
    async with pg_session.begin():
        rubric_dal = RubricDAL(pg_session, es_session)
        rubrics = await rubric_dal.get_20_rubrics_by_text(text=text)
        if rubrics is None:
            return
    return [ShowRubric(id=rubric.id, text=rubric.text, rubrics=rubric.rubrics, created_date=rubric.created_date)
            for rubric in rubrics]


async def _delete_rubric_by_id(id: int, pg_session: AsyncSession, es_session: AsyncElasticsearch) -> DeletedRubric | None:
    async with pg_session.begin():
        rubric_dal = RubricDAL(pg_session, es_session)
        deleted_id = await rubric_dal.delete_rubric_by_id(id=id)
        if deleted_id is None:
            return

    return DeletedRubric(id=deleted_id)
