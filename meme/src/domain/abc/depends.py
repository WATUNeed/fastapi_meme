from typing import Annotated

from fastapi import Query, Depends

from src.domain.abc.dto import PaginationDTO


def _get_pagination(offset: int = Query(0, ge=0), limit: int = Query(10, le=10)) -> PaginationDTO:
    return PaginationDTO(
        offset=offset,
        limit=limit
    )


get_pagination = Annotated[
    PaginationDTO, Depends(_get_pagination)
]

