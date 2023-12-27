import json

from aio_pika import DeliveryMode, Message, connect

from settings import RABBIT_URL


async def set_task(queue: str, **args) -> None:
    connection = await connect(RABBIT_URL)

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue(
            queue,
            durable=True,
        )

        message = Message(
            body=json.dumps(args).encode('utf-8'),
            delivery_mode=DeliveryMode.PERSISTENT,
        )

        await channel.default_exchange.publish(message=message, routing_key=queue.name)
