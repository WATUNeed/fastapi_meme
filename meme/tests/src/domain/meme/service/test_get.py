from uuid import uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.meme.dto import MemeGetDTO
from src.domain.meme.exception import MemeExceptions
from src.domain.meme.service import meme_get
from tests.fixture.utils import generate_string


@pytest.mark.asyncio
class TestMemeGetService:
    @pytest.mark.parametrize(
        'meme',
        [
            {
                'meme': {
                    'name': generate_string(256),
                    'description': generate_string(256),
                    'image_id': uuid4()
                }
            }
        ],
        indirect=True
    )
    async def test_standard(
            self, session: AsyncSession, meme: MemeGetDTO
    ):
        meme_ = await meme_get(session, meme.id)
        assert meme_ == meme

    async def test_not_found(
            self, session: AsyncSession
    ):
        with pytest.raises(type(MemeExceptions.NotFound)) as exc:
            await meme_get(session, uuid4())
        assert exc.value == MemeExceptions.NotFound, f'{repr(exc.value)} == {repr(MemeExceptions.NotFound)}'

