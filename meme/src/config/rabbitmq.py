from faststream.rabbit import RabbitExchange
from faststream.rabbit.utils import build_url
from pydantic_settings import BaseSettings, SettingsConfigDict


class RabbitMQConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='RABBITMQ_')

    host: str
    port: int
    default_user: str
    default_pass: str
    vhost: str

    def connection_url(self):
        return build_url(
            host=self.host, port=self.port, login=self.default_user, password=self.default_pass, virtualhost=self.vhost
        )


RABBITMQ_CONFIG = RabbitMQConfig()

MEME_EXCHANGE = RabbitExchange("MEME", auto_delete=True)
MEDIA_EXCHANGE = RabbitExchange("MEDIA", auto_delete=True)
