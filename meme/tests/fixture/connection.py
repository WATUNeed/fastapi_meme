import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.postgres.connection import Session


@pytest_asyncio.fixture()
async def session() -> AsyncSession:
    session_ = Session()
    try:
        yield session_
    except Exception as exc:
        raise exc
    finally:
        await session_.rollback()
        await session_.close()