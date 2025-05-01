from fastapi import FastAPI
from api.v1.routes import pipelines as pipelines_v1
from api.v1.routes import pipeline_runs as pipeline_runs_v1

app = FastAPI()

app.include_router(pipelines_v1.router, prefix="/api/v1")
app.include_router(pipeline_runs_v1.router, prefix="/api/v1")