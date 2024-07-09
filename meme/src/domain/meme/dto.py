from uuid import UUID

from pydantic import Field

from src.domain.abc.dto import AbstractDTO


class MemeCreateDTO(AbstractDTO):
    name: str = Field(..., max_length=256)
    description: str | None = Field(None)
    # image: bytes = Field(...)


class MemeGetDTO(AbstractDTO):
    id: UUID = Field(...)
    name: str = Field(..., max_length=256)
    description: str | None = Field(None)
    image_id: UUID = Field(...)
    image_url: str = Field(...)


class MemeUpdateDTO(AbstractDTO):
    id: UUID = Field(...)
    name: str | None = Field(None, max_length=256)
    description: str | None = Field(None)
    image: bytes | None = Field(None)
