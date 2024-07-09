from uuid import UUID

from faststream.rabbit import RabbitRouter

from src.api.amqp.exchange import MEDIA_EXCHANGE
from src.api.amqp.meme.queue import MemeQueues
from src.domain.meme.service import meme_create, meme_get

meme_amqp_v1 = RabbitRouter()


@meme_amqp_v1.subscriber(
    queue=MemeQueues.create,
    exchange=MEDIA_EXCHANGE
)
async def meme_create_consumer(image: bytes) -> UUID:
    filename = await meme_create(image)
    return filename


@meme_amqp_v1.subscriber(
    queue=MemeQueues.get,
    exchange=MEDIA_EXCHANGE
)
async def meme_get_consumer(filename: UUID) -> bytes:
    meme = await meme_get(filename)
    return meme
