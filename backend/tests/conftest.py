import asyncio
import datetime
from typing import List, Any, Generator

import asyncpg
from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

import settings
from db.es.indexes import INDEX_RUBRICS
from db.pg.session_pg import get_db_pg
from main import app
import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.PG_DATABASE_URL, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession,
                                 autocommit=False,
                                 autoflush=False, )
    yield async_session


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool("".join(settings.PG_DATABASE_URL.split("+asyncpg")))
    yield pool
    await pool.close()


@pytest.fixture(scope="function")
async def test_async_client_es() -> AsyncElasticsearch:
    test_async_client_es = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    try:
        yield test_async_client_es
    finally:
        await test_async_client_es.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_tables_pg(async_session_test):
    async with async_session_test() as session:
        async with session.begin():
            await session.execute(
                text(f"TRUNCATE TABLE rubrics")
            )


@pytest.fixture(scope="function", autouse=True)
async def clean_index(test_async_client_es: AsyncElasticsearch):
    await test_async_client_es.delete_by_query(
        index=INDEX_RUBRICS, query={"match_all": {}}, refresh=True
    )


async def create_rubric(asyncpg_pool, rubric_id: int, rubrics: List[str], text: str, created_date: datetime.datetime) -> int:
    async with asyncpg_pool.acquire() as connection:
        await connection.execute(
            """INSERT INTO rubrics (id, rubrics, text, created_date) VALUES ($1, $2, $3, $4)""",
            rubric_id,
            rubrics,
            text,
            created_date,
        )
        client_es = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
        await client_es.index(
            index=INDEX_RUBRICS,
            document={"id": rubric_id, "text": text},
            refresh=True,
        )
        return rubric_id


async def _get_test_db_pg():
    test_engine = create_async_engine(
        settings.PG_DATABASE_URL, future=True, echo=True
    )

    test_async_session = sessionmaker(
        test_engine, expire_on_commit=False, class_=AsyncSession
    )
    async_session = test_async_session()
    try:
        yield async_session
    finally:
        await async_session.close()


@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `get_db` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[get_db_pg] = _get_test_db_pg
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client
