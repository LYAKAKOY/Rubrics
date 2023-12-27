import asyncio
import json
from logging import getLogger

import elastic_transport
from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from elasticsearch import AsyncElasticsearch
import settings
from db.elasticsearch.indexes import INDEX_RUBRICS

logger = getLogger(__name__)


def restart():
    import sys
    import os
    os.execv(sys.executable, ['python'] + sys.argv)


async def create_document_es(message: AbstractIncomingMessage) -> None:
    es_session = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL, retry_on_timeout=True, max_retries=10)
    param = json.loads(message.body.decode('utf-8'))
    try:
        res_es = await es_session.index(
            index=INDEX_RUBRICS,
            document=param,
            refresh=True
        )
        if res_es.meta.status == 201:
            logger.info(f"{message.message_id} has been done!")
            await message.ack()
    except elastic_transport.ConnectionError as err:
        logger.error(err)
        restart()
    finally:
        await es_session.close()


async def delete_document_es(message: AbstractIncomingMessage) -> None:
    es_session = AsyncElasticsearch(hosts=settings.ES_DATABASE_URL, retry_on_timeout=True, max_retries=10)
    param = json.loads(message.body.decode('utf-8'))
    try:
        res_es = await es_session.delete_by_query(
            index=INDEX_RUBRICS,
            query={"term": {"id": {"value": param["id"]}}},
            refresh=True,
        )
        if res_es.meta.status == 200:
            logger.info(f"{message.message_id} has been done!")
            await message.ack()
    except elastic_transport.ConnectionError as err:
        logger.error(err)
        restart()
    finally:
        await es_session.close()


async def main() -> None:
    connection = await connect(settings.RABBIT_URL)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=1)

        queue_create = await channel.declare_queue(
            settings.RABBIT_QUEUE_CREATE_TASK,
            durable=True,
        )
        await queue_create.consume(create_document_es)

        queue_delete = await channel.declare_queue(
            settings.RABBIT_QUEUE_DELETE_TASK,
            durable=True,
        )
        await queue_delete.consume(delete_document_es)
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
