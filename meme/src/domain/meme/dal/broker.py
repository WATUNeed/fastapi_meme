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

    @classmethod
    async def create(cls, meme: bytes) -> UUID | None:
        result = await BROKER.publish(meme, cls._Queues.create, MEDIA_EXCHANGE, rpc=True, rpc_timeout=1)
        if result is None or result == b'':
            return None
        return result

    @classmethod
    async def get(cls, image_id: UUID) -> bytes | None:
        filename = f'{image_id}'
        result = await BROKER.publish(filename, cls._Queues.get, MEDIA_EXCHANGE, rpc=True, rpc_timeout=1)
        if result is None or result == b'':
            return None
        return result