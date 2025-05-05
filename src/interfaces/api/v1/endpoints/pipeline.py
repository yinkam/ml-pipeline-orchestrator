from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated, Dict

from src.domain.entities.pipeline import PipelineDto, PipelineCreateDto
from src.domain.use_cases.pipeline import PipelineUseCase

pipeline_router = APIRouter(prefix="/pipelines", tags=["pipelines"])


@pipeline_router.post("/", response_model=PipelineDto, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
        pipeline_data: PipelineCreateDto,
        use_case: Annotated[PipelineUseCase, Depends()]):
    """Endpoint to create a new pipeline."""

    try:
        return await use_case.create_pipeline(pipeline_data)
    except HTTPException as e:
        raise e


@pipeline_router.get("/", response_model=Dict[str, List[PipelineDto]], status_code=status.HTTP_200_OK)
async def get_all_pipelines(use_case: Annotated[PipelineUseCase, Depends()]):
    """Endpoint to get all use_cases."""

    return await use_case.get_all_pipelines()


@pipeline_router.get("/{pipeline_id}", response_model=PipelineDto, status_code=status.HTTP_200_OK)
async def get_pipeline(pipeline_id: int, use_case: Annotated[PipelineUseCase, Depends()],):
    """Endpoint to get a pipeline by its ID."""

    try:
        return await use_case.get_pipeline(pipeline_id)
    except HTTPException as e:
        raise e

