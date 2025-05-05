import logging

from fastapi import Depends, HTTPException, status
from typing import Annotated, Dict, List

from src.domain.entities.run import RunCreateDto, RunDto
from src.domain.repositories.interface import RunRepositoryInterface
from src.domain.use_cases.pipeline import PipelineUseCase
from src.interfaces.database.repositories.run_repository import RunRepository

logger = logging.getLogger(__name__)

class RunUseCase:
    def __init__(self,
        repo: Annotated[RunRepositoryInterface, Depends(RunRepository)],
        pipeline_use_case: Annotated[PipelineUseCase, Depends()]
    ):
        self.repo = repo
        self.pipeline_use_case = pipeline_use_case


    async def create_pipeline_run(self, pipeline_id: int, run_create: RunCreateDto) -> RunDto:
        """
        UseCase to create a new pipeline.
        """

        await self.validate_pipeline(pipeline_id=pipeline_id)

        try:
            db_run = await self.repo.create(run_create)
            return RunDto.model_validate(db_run)
        except HTTPException as e:
            raise e

    async def get_all_pipeline_runs(self, pipeline_id: int) -> Dict[str, List[RunDto]]:
        """
        UseCase to get all pipeline runs.
        """
        await self.validate_pipeline(pipeline_id=pipeline_id)

        try:
            db_runs = await self.repo.get_all_by_pipeline_id(pipeline_id)
            runs = [RunDto.model_validate(r) for r in db_runs]
            return dict(pipeline_id=pipeline_id, runs=runs)
        except HTTPException as e:
            raise e


    async def get_pipeline_run(self, pipeline_id: int, run_id: int) -> RunDto:
        """
        UseCase to retrieve a pipeline run by its ID.
        """
        await self.validate_pipeline(pipeline_id=pipeline_id)

        try:
            run = await self.repo.get_by_id(run_id)
        except HTTPException as e:
            raise e

        if not run:
            logger.warning(f"Run with ID '{run_id}' not found.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Run with ID {run_id} not found.")
        if run.pipeline_id != pipeline_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Run with ID {run_id} does not belong to pipeline with ID {pipeline_id}",
            )
        return RunDto.model_validate(run)


    async def validate_pipeline(self, pipeline_id: int):
        pipeline = await self.pipeline_use_case.get_pipeline(pipeline_id)
        if not pipeline:
            raise HTTPException(status_code=404, detail=f"Pipeline with ID {pipeline_id} not found")