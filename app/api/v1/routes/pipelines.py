from fastapi import APIRouter, HTTPException

router = APIRouter(prefix='/pipelines', tags=['pipelines'])

@router.post("/")
def create_pipeline():
    pass

@router.get("/")
def get_all_pipelines():
    pass

@router.get("/{pipeline_id}")
def get_pipeline():
    pass

@router.post("/{pipeline_id}/trigger_run")
def trigger_pipeline_run():
    pass