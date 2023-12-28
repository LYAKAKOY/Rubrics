import asyncio
from typing import Any
from typing import Generator

import pytest
import settings
from db.es.indexes import INDEX_RUBRICS
from db.pg.session_pg import async_session
from elasticsearch import AsyncElasticsearch
from httpx import AsyncClient
from main import app
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def client() -> Generator[AsyncClient, Any, None]:
    async with AsyncClient(app=app, base_url="http://127.0.0.1") as client:
        yield client


@pytest.fixture(scope="function")
async def test_async_client_es() -> AsyncElasticsearch:
    test_async_client_es = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL)
    try:
        yield test_async_client_es
    finally:
        await test_async_client_es.close()


@pytest.fixture(scope="function")
async def test_async_client_pg() -> AsyncSession:
    db_session = async_session()
    try:
        yield db_session
    finally:
        await db_session.close()


@pytest.fixture(scope="function", autouse=True)
async def clean_index(test_async_client_es: AsyncElasticsearch):
    await test_async_client_es.delete_by_query(
        index=INDEX_RUBRICS, query={"match_all": {}}, refresh=True
    )


@pytest.fixture(scope="function", autouse=True)
async def clean_table(test_async_client_pg: AsyncSession):
    async with test_async_client_pg.begin():
        await test_async_client_pg.execute(text("TRUNCATE TABLE rubrics"))
