from fastapi import APIRouter, status

memes_rest_v1 = APIRouter(
    tags=["Memes"],
    prefix='/memes'
)


@memes_rest_v1.post(
    path='',
    status_code=status.HTTP_201_CREATED,
    response_model=...,
)
async def meme_create():
    pass
