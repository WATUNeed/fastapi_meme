from uuid import UUID

from src.domain.meme.dao import MemeDAO


async def meme_create(image: bytes) -> UUID:
    filename = MemeDAO().create(image)
    return filename


async def meme_get(filename: UUID) -> bytes:
    meme = MemeDAO().get_by_name(filename)
    return meme
