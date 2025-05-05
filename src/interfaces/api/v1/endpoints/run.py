from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated

from src.domain.entities.run import RunDto, RunCreateDto, RunCreateRequest, RunResponse
from src.domain.use_cases.run import RunUseCase

run_router = APIRouter(prefix="/pipeline/{pipeline_id}", tags=["runs"])


@run_router.post("/trigger_run", response_model=RunDto, status_code=status.HTTP_201_CREATED)
async def create_pipeline_run(
        pipeline_id: int,
        run_create_request: RunCreateRequest,
        use_case: Annotated[RunUseCase, Depends()]):
    """
    Endpoint to create a new run for a given pipeline.
    """
    try:
        run_data = RunCreateDto(pipeline_id=pipeline_id, **run_create_request.model_dump())
        run = await use_case.create_pipeline_run(pipeline_id=pipeline_id, run_create=run_data)
        return run
    except HTTPException as e:
        raise e

@run_router.get("/runs", response_model=RunResponse, status_code=status.HTTP_200_OK)
async def get_all_pipeline_runs(pipeline_id, use_case: Annotated[RunUseCase, Depends()]):
    """
    Endpoint to get all runs for a given pipeline.
    """
    try:
        return await use_case.get_all_pipeline_runs(pipeline_id)
    except HTTPException as e:
        raise e

@run_router.get("/runs/{run_id}", response_model=RunDto, status_code=status.HTTP_200_OK)
async def get_pipeline_run(pipeline_id: int, run_id: int, use_case: Annotated[RunUseCase, Depends()]):
    """
    Endpoint to get a specific run for a given pipeline.
    """
    try:
        return await use_case.get_pipeline_run(pipeline_id=pipeline_id, run_id=run_id)
    except HTTPException as e:
        raise e