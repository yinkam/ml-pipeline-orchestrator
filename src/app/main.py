from fastapi import FastAPI

from src.interfaces.api.v1.endpoints.pipeline import pipeline_router
from src.interfaces.api.v1.endpoints.run import run_router



app = FastAPI()

VERSION = 'v1'

app.include_router(pipeline_router, prefix=f"/api/{VERSION}")
app.include_router(run_router, prefix=f"/api/{VERSION}")
