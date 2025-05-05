import logging
from fastapi import Depends, HTTPException
from typing import Annotated, List, Dict

from src.domain.repositories.interface import PipelineRepositoryInterface
from src.domain.entities.pipeline import PipelineCreateDto, PipelineDto
from src.interfaces.database.repositories.pipeline_repository import PipelineRepository

logger = logging.getLogger(__name__)


class PipelineUseCase:
    """
    UseCase for managing pipeline business logic.
    """

    def __init__(self, repo: Annotated[PipelineRepositoryInterface, Depends(PipelineRepository)]):
        self.repo = repo

    async def create_pipeline(self, pipeline_data: PipelineCreateDto) -> PipelineDto:
        """
        Creates a new pipeline.
        """
        try:
            db_pipeline = await self.repo.create(pipeline_data)
            return PipelineDto.model_validate(db_pipeline)
        except HTTPException as e:
            logger.error(f"Error creating pipeline: {e}")
            raise e

    async def get_all_pipelines(self) -> Dict[str, List[PipelineDto]]:
        """
        Retrieves all pipelines.
        """
        try:
            db_pipelines = await self.repo.get_all()
            pipelines = [PipelineDto.model_validate(p) for p in db_pipelines]

            return dict(pipelines=pipelines)
        except HTTPException as e:
            raise e

    async def get_pipeline(self, pipeline_id: int) -> PipelineDto:
        """
        Retrieves a pipeline by its ID.
        """
        try:
            pipeline = await self.repo.get_by_id(pipeline_id)
            return PipelineDto.model_validate(pipeline)
        except HTTPException as e:
            logger.error(f"Error retrieving pipeline {pipeline_id}: {e}")
            raise e