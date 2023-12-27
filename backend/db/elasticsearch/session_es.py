from typing import Generator

import settings
from elasticsearch import AsyncElasticsearch


async def get_db_es() -> Generator:
    es_session = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL, retry_on_timeout=True, max_retries=10)
    try:
        yield es_session
    finally:
        await es_session.close()