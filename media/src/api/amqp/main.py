from faststream import FastStream
from faststream.rabbit import RabbitBroker

from src.config.rabbitmq import RABBITMQ_CONFIG

BROKER = RabbitBroker(RABBITMQ_CONFIG.connection_url())
app = FastStream(BROKER)

@app.on_startup
async def on_startup():
    from src.api.amqp.meme.consumer import meme_amqp_v1
    BROKER.include_routers(
        meme_amqp_v1
    )
