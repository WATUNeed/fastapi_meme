import pytest
from faststream.rabbit import RabbitBroker, TestRabbitBroker

from src.api.amqp.main import BROKER


@pytest.fixture(scope='function')
async def broker() -> RabbitBroker:
    async with TestRabbitBroker(BROKER, with_real=True) as broker_:
        broker_.include_routers(
            raise
        )
        yield broker_