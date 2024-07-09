from uuid import UUID

from fastapi import APIRouter, status, Response

from src.domain.meme.dal.broker import MemeBrokerDAO

images_rest_v1 = APIRouter(
    tags=["Images"],
    prefix='/images'
)


@images_rest_v1.get(
    path='/{image_id}',
    responses={status.HTTP_200_OK: {'content': {f'image/png': {}}}},
)
async def get_image(image_id: UUID):
    content = await MemeBrokerDAO.get(image_id)
    return Response(content=content, media_type=f'image/png')