from typing import Generator

import settings
from elasticsearch import AsyncElasticsearch


async def get_db_es() -> Generator:
    elastic_client = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL, retry_on_timeout=True, max_retries=10)
    try:
        yield elastic_client
    finally:
        await elastic_client.close()