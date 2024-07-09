from uuid import UUID, uuid4

import pytest
from faker import Faker
from sqlalchemy.exc import DatabaseError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.meme.dal.sql import MemeSQLDAO
from src.domain.meme.dto import MemeCreateDTO
from tests.fixture.utils import generate_string


async def _assert_success(
        session: AsyncSession, name: str, description: str | None, image_id: UUID
):
    data = MemeCreateDTO(
        name=name,
        description=description
    )
    result = await MemeSQLDAO(session).create(data, image_id=image_id)
    assert result.name == data.name
    assert result.description == data.description
    assert result.image_id == image_id


async def _assert_error(
        session: AsyncSession,
        data: MemeCreateDTO,
        image_id: UUID | None,
        error_message: str
):
    with pytest.raises((DatabaseError, DBAPIError)) as e:
        await MemeSQLDAO(session).create(data, image_id=image_id)
    assert error_message in str(e.value)


FAKER = Faker()


@pytest.mark.asyncio
@pytest.mark.parametrize('name', [generate_string(256)])
@pytest.mark.parametrize('description', [generate_string(256)])
@pytest.mark.parametrize('image_id', [uuid4()])
class TestMemeDAOCreate:
    async def test_standard(
            self, session: AsyncSession, name: str, description: str, image_id: UUID
    ):
        await _assert_success(session, name, description, image_id)

    async def test_name_not_selected(
            self,
            session: AsyncSession, name: str, description: str, image_id: UUID
    ):
        data = MemeCreateDTO(
            name=name,
            description=description
        )
        data.name = None
        await _assert_error(
            session,
            data,
            image_id,
            'null value in column "name" of relation "meme_table" violates not-null constraint'
        )

    async def test_description_not_selected(
            self, session: AsyncSession, name: str, description: str, image_id: UUID
    ):
        description = None
        await _assert_success(session, name, description, image_id)

    async def test_image_id_not_selected(
            self,
            session: AsyncSession, name: str, description: str, image_id: UUID
    ):
        data = MemeCreateDTO(
            name=name,
            description=description
        )
        image_id = None
        await _assert_error(
            session,
            data,
            image_id,
            'null value in column "image_id" of relation "meme_table" violates not-null constraint'
        )
