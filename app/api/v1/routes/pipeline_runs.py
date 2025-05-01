from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/pipelines/{pipeline_id}/runs', tags=['pipeline_runs'])


@router.get("/")
def get_all_pipeline_runs():
    pass

@router.get("/{run_id}")
def get_pipeline_run():
    pass

