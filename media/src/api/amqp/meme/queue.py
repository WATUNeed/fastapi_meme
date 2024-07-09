from faststream.rabbit import RabbitQueue

from src.config.rabbitmq import RABBITMQ_CONFIG


class MemeQueues:
    _domain = 'meme'
    _v = 'v1'

    create = RabbitQueue(f'{_v}.{_domain}_create', **RABBITMQ_CONFIG.queue_factory())
    get = RabbitQueue(f'{_v}.{_domain}_get', **RABBITMQ_CONFIG.queue_factory())
    get_names = RabbitQueue(f'{_v}.{_domain}_get_names', **RABBITMQ_CONFIG.queue_factory())