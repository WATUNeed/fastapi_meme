from typing import List

from sqlalchemy import select

from src.domain.abc.dao import AbstractDAO
from src.domain.abc.dto import PaginationDTO
from src.domain.meme.dto import MemeGetDTO, MemeCreateDTO, MemeUpdateDTO
from src.domain.meme.model import Meme


class MemeSQLDAO(
    AbstractDAO[
        Meme,
        MemeGetDTO,
        MemeCreateDTO,
        MemeUpdateDTO
    ]
):
    model = Meme
    get_dto = MemeGetDTO
    create_dto = MemeCreateDTO
    update_dto = MemeUpdateDTO

    async def get_list_with_pagination(self, pagination: PaginationDTO) -> List[get_dto]:
        query = select(
            self.model
        ).offset(
            pagination.limit * pagination.offset
        ).limit(
            pagination.limit
        )

        result = (await self.session.scalars(query)).all()

        if len(result) < 1:
            return []
        return [
            self.get_dto.model_validate(
                meme
            )
            for meme in result
        ]
