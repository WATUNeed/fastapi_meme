import pytest_asyncio
from _pytest.fixtures import SubRequest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc.dto import AbstractDTO
from src.domain.meme.dal.sql import MemeSQLDAO
from src.domain.meme.dto import MemeGetDTO


@pytest_asyncio.fixture
async def meme(request: SubRequest, session: AsyncSession) -> MemeGetDTO:
    meme = await MemeSQLDAO(session).create(
        AbstractDTO(),
        **request.param['meme']
    )
    return meme