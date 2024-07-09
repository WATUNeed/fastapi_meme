from typing import Set
from uuid import UUID

from src.domain.meme.dao import MemeDAO


async def meme_create(image: bytes) -> UUID:
    filename = MemeDAO().create(image)
    return filename


async def meme_get(filename: UUID) -> bytes:
    meme = MemeDAO().get_by_name(filename)
    return meme


async def meme_get_names() -> Set[UUID]:
    memes_names = MemeDAO().get_names_from_bucket()
    return memes_names
