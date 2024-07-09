from typing import List
from uuid import UUID

from fastapi import APIRouter, status, Body, Path

from src.database.postgres.depends import get_session
from src.domain.abc.depends import get_pagination
from src.domain.meme.dto import MemeCreateDTO, MemeGetDTO, MemeUpdateDTO
from src.domain.meme.service import meme_create, meme_get, memes_get, meme_update, meme_delete


memes_rest_v1 = APIRouter(
    tags=["Memes"],
    prefix='/memes'
)


@memes_rest_v1.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=MemeGetDTO,
)
async def meme_create_route(session: get_session, body: MemeCreateDTO = Body(...)):
    new_meme = await meme_create(session, body)
    return new_meme


@memes_rest_v1.put(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=MemeGetDTO,
)
async def meme_update_route(session: get_session, body: MemeUpdateDTO = Body(...)):
    meme = await meme_update(session, body)
    return meme


@memes_rest_v1.get(
    path='/{id}',
    status_code=status.HTTP_200_OK,
    response_model=MemeGetDTO,
)
async def meme_get_route(session: get_session, id: UUID = Path(...)):
    meme = await meme_get(session, id)
    return meme


@memes_rest_v1.delete(
    path='/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def meme_delete_route(session: get_session, id: UUID = Path(...)):
    await meme_delete(session, id)


@memes_rest_v1.get(
    path='',
    status_code=status.HTTP_200_OK,
    response_model=List[MemeGetDTO],
)
async def memes_get_route(session: get_session, pagination: get_pagination):
    memes = await memes_get(session, pagination)
    return memes
