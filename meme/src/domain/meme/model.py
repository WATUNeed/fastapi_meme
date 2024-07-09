import uuid

from sqlalchemy import UUID, func, String
from sqlalchemy.orm import Mapped, mapped_column, synonym

from src.config.meme import MEME_CONFIG
from src.domain.abc.model import AbstractModel


class Meme(AbstractModel):
    __tablename__ = 'meme_table'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    image_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)

    @property
    def image_url(self) -> str:
        return f'{MEME_CONFIG.origin}/api/v1/images/{self.image_id}'

    image_url = synonym('image_id', descriptor=image_url)
