from typing import Dict, Any

from pydantic_settings import SettingsConfigDict, BaseSettings


class MemeConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='MEME_')

    debug: bool
    host: str
    port: int
    origin: str

    def init_kwargs(self) -> Dict[str, Any]:
        if self.debug is False:
            addition = {
                'openapi_url': None,
                'docs_url': None,
                'redoc_url': None,
                'swagger_ui_oauth2_redirect_url': None
            }
        else:
            addition = {}

        return {
            **addition,
            'title': 'Meme',
            'description': 'Тестовое задание',
            'debug': self.debug,
        }


MEME_CONFIG = MemeConfig()
