from uuid import uuid4, UUID

import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.meme.dto import MemeCreateDTO
from src.domain.meme.exception import MemeExceptions
from src.domain.meme.service import meme_create
from tests.fixture.utils import generate_string, IMAGE_BYTES

faker = Faker()


@pytest.mark.asyncio
@pytest.mark.parametrize('name', [generate_string(256)])
@pytest.mark.parametrize('description', [generate_string(256)])
class TestMemeCreateService:
    @pytest.mark.parametrize(
        'external_mocker',
        [
            {
                'function_path': 'src.domain.meme.dal.broker.MemeBrokerDAO.create',
                'return_value': uuid4()
            }
        ],
        indirect=True
    )
    async def test_standard(
            self, session: AsyncSession, name: str, description: str, external_mocker: UUID
    ):
        data = MemeCreateDTO(
            name=name,
            description=description,
        )
        new_meme = await meme_create(session, data, IMAGE_BYTES)
        assert new_meme.name == name
        assert new_meme.description == description
        assert new_meme.image_id == external_mocker

    @pytest.mark.parametrize(
        'external_mocker',
        [
            {
                'function_path': 'src.domain.meme.dal.broker.MemeBrokerDAO.create',
                'return_value': None
            }
        ],
        indirect=True
    )
    async def test_file_not_saved(
            self, session: AsyncSession, name: str, description: str, external_mocker: None
    ):
        data = MemeCreateDTO(
            name=name,
            description=description,
        )
        with pytest.raises(type(MemeExceptions.NotSaved)) as exc:
            await meme_create(session, data, IMAGE_BYTES)
        assert exc.value == MemeExceptions.NotSaved, f'{repr(exc.value)} == {repr(MemeExceptions.NotSaved)}'
