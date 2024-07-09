import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from src.api.amqp.main import BROKER
from src.config.meme import MEME_CONFIG
from src.utils.routers_utils import include_routers


@asynccontextmanager
async def lifespan(app_: FastAPI):
    os.system('alembic upgrade head')

    v1_routers = []
    v1_router = include_routers(APIRouter(prefix='/v1'), v1_routers)
    main_router = include_routers(APIRouter(prefix='/api'), (v1_router,))
    app_.include_router(main_router)

    await BROKER.connect()
    yield
    await BROKER.close()


app = FastAPI(**MEME_CONFIG.init_kwargs(), lifespan=lifespan)
