from typing import Generator
import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(settings.PG_DATABASE_URL, echo=False)

AsyncSession = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db() -> Generator:
    db_session = AsyncSession()
    try:
        yield db_session
    finally:
        await db_session.close()
