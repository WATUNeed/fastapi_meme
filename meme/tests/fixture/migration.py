import os

import pytest
from sqlalchemy import text

from src.database.postgres.connection import Session


@pytest.fixture(scope='session', autouse=True)
def migration(_session_event_loop):
    async def delete_old_data():
        sql = text('DROP SCHEMA public CASCADE')
        sql2 = text('CREATE SCHEMA public;')
        sql3 = text('GRANT ALL ON SCHEMA public TO postgres;')
        sql4 = text('GRANT ALL ON SCHEMA public TO public;')
        async with Session() as session:
            await session.execute(sql)
            await session.execute(sql2)
            await session.execute(sql3)
            await session.execute(sql4)
            await session.commit()
            await session.close()

    _session_event_loop.run_until_complete(delete_old_data())

    os.system('alembic upgrade head')