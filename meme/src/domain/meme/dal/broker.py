from typing import Set
from uuid import UUID

from faststream.rabbit import RabbitQueue

from src.api.amqp.exchange import MEDIA_EXCHANGE
from src.api.amqp.main import BROKER
from src.config.rabbitmq import RABBITMQ_CONFIG


class MemeBrokerDAO:
    class _Queues:
        _domain = 'meme'
        _v = 'v1'

        create = RabbitQueue(f'{_v}.{_domain}_create', **RABBITMQ_CONFIG.queue_factory())
        get = RabbitQueue(f'{_v}.{_domain}_get', **RABBITMQ_CONFIG.queue_factory())
        get_names = RabbitQueue(f'{_v}.{_domain}_get_names', **RABBITMQ_CONFIG.queue_factory())

    @classmethod
    async def create(cls, meme: bytes) -> UUID | None:
        result = await BROKER.publish(meme, cls._Queues.create, MEDIA_EXCHANGE, rpc=True)
        if result is None or result == b'':
            return None
        return result

    @classmethod
    async def get(cls, image_id: UUID) -> bytes:
        filename = f'{image_id}'
        result = await BROKER.publish(filename, cls._Queues.get, MEDIA_EXCHANGE, rpc=True)
        if result is None or result == b'':
            return None
        return result

    @classmethod
    async def get_names(cls) -> Set[UUID]:
        result = await BROKER.publish(None, cls._Queues.get_names, MEDIA_EXCHANGE, rpc=True)
        if result is None or result == b'':
            return None
        return result