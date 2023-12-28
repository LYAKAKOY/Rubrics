from typing import List

from elasticsearch import AsyncElasticsearch
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.rubrics import _create_rubric, _get_20_rubrics_by_text, _delete_rubric_by_id
from api.rubrics.schemas import ShowRubric, CreateRubric, DeletedRubric
from db.es.session_es import get_db_es
from db.pg.session_pg import get_db_pg


rubrics_router = APIRouter()


@rubrics_router.post("/")
async def create_rubric(
        body: CreateRubric,
        pg_session: AsyncSession = Depends(get_db_pg),
        es_session: AsyncElasticsearch = Depends(get_db_es)
):
    res = await _create_rubric(rubric=body, pg_session=pg_session, es_session=es_session)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="the server is not responding",
        )
    return res


@rubrics_router.get("/{text}", response_model=List[ShowRubric])
async def get_rubrics_by_text(
        text: str,
        pg_session: AsyncSession = Depends(get_db_pg),
        es_session: AsyncElasticsearch = Depends(get_db_es)
) -> List[ShowRubric]:
    res = await _get_20_rubrics_by_text(text=text, pg_session=pg_session, es_session=es_session)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the rubrics not found",
        )
    return res


@rubrics_router.delete("/{id}", response_model=DeletedRubric)
async def delete_rubric_by_id(
        id: int,
        pg_session: AsyncSession = Depends(get_db_pg),
        es_session: AsyncElasticsearch = Depends(get_db_es)
) -> DeletedRubric:
    res = await _delete_rubric_by_id(id=id, pg_session=pg_session, es_session=es_session)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="the rubrics not found",
        )
    return res
