import os
from envparse import Env

env = Env()

PG_DATABASE_URL: str = env.str(
    "DATABASE_URL",
    default=f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@"
            f"{os.environ.get('PG_DATABASE')}:{os.environ.get('POSTGRES_PORT')}/{os.environ.get('POSTGRES_DB')}",
)

ES_DATABASE_URL: str = env.str(
    "ES_DATABASE_URL",
    default=f"http://{os.environ.get('ES_DATABASE')}:{os.environ.get('ES_PORT')}",
)

RABBIT_URL: str = env.str(
    "RABBIT_URL", default=f"amqp://{os.environ.get('RABBIT_USER')}:{os.environ.get('RABBIT_PASSWORD')}"
                          f"@{os.environ.get('RABBITMQ')}:{os.environ.get('RABBIT_PORT')}//"
)

RABBIT_QUEUE_CREATE_TASK: str = env.str("RABBIT_QUEUE_CREATE_TASK", default="tasks_create")
RABBIT_QUEUE_DELETE_TASK: str = env.str("RABBIT_QUEUE_DELETE_TASK", default="tasks_delete")

SCROLL_TIME: str = env.str(
    "SCROLL_TIME",
    default="15m",
)