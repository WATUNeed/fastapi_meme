from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc.dto import PaginationDTO
from src.domain.meme.dal.broker import MemeBrokerDAO
from src.domain.meme.dal.sql import MemeSQLDAO
from src.domain.meme.dto import MemeCreateDTO, MemeGetDTO, MemeUpdateDTO
from src.domain.meme.exception import MemeExceptions


async def meme_create(session: AsyncSession, data: MemeCreateDTO, image: bytes) -> MemeGetDTO:
    image_id = await MemeBrokerDAO.create(image)
    if image_id is None:
        raise MemeExceptions.NotSaved
    new_meme = await MemeSQLDAO(session).create(data, image_id=image_id)
    return new_meme


async def meme_update(session: AsyncSession, data: MemeUpdateDTO) -> MemeGetDTO:
    meme = await MemeSQLDAO(session).get_dto_by_id(id)
    if meme is None:
        raise MemeExceptions.NotFound

    image_id = meme.image_id

    if data.image is not None:
        image_id = await MemeBrokerDAO.create(data.image)
        if image_id is None:
            raise MemeExceptions.NotSaved

    meme = await MemeSQLDAO(session).update(data, exclude={'image'}, image_id=image_id)
    return meme


async def meme_delete(session: AsyncSession, id: UUID):
    meme = await MemeSQLDAO(session).get_dto_by_id(id)
    if meme is None:
        raise MemeExceptions.NotFound
    await MemeSQLDAO(session).delete(id)


async def meme_get(session: AsyncSession, id: UUID) -> MemeGetDTO:
    meme = await MemeSQLDAO(session).get_dto_by_id(id)
    if meme is None:
        raise MemeExceptions.NotFound
    image = await MemeBrokerDAO.get(meme.image_id)
    if image is None:
        raise MemeExceptions.FileNotFound
    return meme


async def memes_get(session: AsyncSession, pagination: PaginationDTO) -> List[MemeGetDTO]:
    memes = await MemeSQLDAO(session).get_list_with_pagination(pagination)
    return memes
