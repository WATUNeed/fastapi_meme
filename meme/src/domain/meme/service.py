from typing import List
from uuid import uuid4, UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.abc.dto import PaginationDTO
from src.domain.meme.dao import MemeDAO
from src.domain.meme.dto import MemeCreateDTO, MemeGetDTO, MemeUpdateDTO
from src.domain.meme.exception import MemeExceptions


async def meme_create(session: AsyncSession, data: MemeCreateDTO) -> MemeGetDTO:
    new_meme = await MemeDAO(session).create(data, exclude={'image'}, image_id=uuid4())
    return new_meme


async def meme_update(session: AsyncSession, data: MemeUpdateDTO) -> MemeGetDTO:
    meme = await MemeDAO(session).update(data, exclude={'image'}, image_id=uuid4())
    return meme


async def meme_delete(session: AsyncSession, id: UUID):
    meme = await MemeDAO(session).get_dto_by_id(id)
    if meme is None:
        raise MemeExceptions.NotFound
    await MemeDAO(session).delete(id)


async def meme_get(session: AsyncSession, id: UUID) -> MemeGetDTO:
    meme = await MemeDAO(session).get_dto_by_id(id)
    if meme is None:
        raise MemeExceptions.NotFound
    return meme


async def memes_get(session: AsyncSession, pagination: PaginationDTO) -> List[MemeGetDTO]:
    memes = await MemeDAO(session).get_list_with_pagination(pagination)
    return memes
