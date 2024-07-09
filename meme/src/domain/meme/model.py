import uuid

from sqlalchemy import UUID, func, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.abc.model import AbstractModel


class Meme(AbstractModel):
    __tablename__ = 'meme_table'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid.uuid4, server_default=func.gen_random_uuid()
    )

    name: Mapped[str] = mapped_column(String(256), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    image_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)