from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.interfaces.api.v1.endpoints.pipeline import pipeline_router
from src.interfaces.api.v1.endpoints.run import run_router
from src.interfaces.database.core import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

VERSION = 'v1'

app.include_router(pipeline_router, prefix=f"/api/{VERSION}")
app.include_router(run_router, prefix=f"/api/{VERSION}")
