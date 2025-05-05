import logging
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from typing import Annotated

from src.domain.repositories.interface import PipelineRepositoryInterface
from src.interfaces.database.core import get_async_db
from src.interfaces.database.models.pipeline import Pipeline
from src.domain.entities.pipeline import PipelineCreateDto

logger = logging.getLogger(__name__)


class PipelineRepository(PipelineRepositoryInterface):
    """
    Repository for managing Pipeline entities
    """

    def __init__(self, db: Annotated[AsyncSession, Depends(get_async_db)]):
        self.db = db

    async def create(self, data: PipelineCreateDto) -> Pipeline:
        """Creates a new pipeline."""

        db_pipeline = Pipeline(**data.model_dump())
        self.db.add(db_pipeline)
        try:
            await self.db.commit()
            await self.db.refresh(db_pipeline)
            logger.info(f"Pipeline created with ID: {db_pipeline.id}")

            # Eagerly load the 'runs' relationship
            # result = await (self.db.execute(
            #     select(Pipeline).where(id==db_pipeline.id).options(selectinload(Pipeline.runs))))
            # loaded_db_pipeline = result.scalar_one()

            return db_pipeline
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating pipeline: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    async def get_by_id(self, pipeline_id) -> Pipeline:
        """Retrieves a pipeline by the ID."""

        try:
            result = await self.db.execute(
                select(Pipeline)
                .filter_by(id=pipeline_id)
            )
            pipeline = result.scalar_one_or_none()
            if not pipeline:
                logger.warning(f"Pipeline with ID '{pipeline_id}' not found in the database.")
                raise HTTPException(status_code=404, detail=f"Pipeline '{pipeline_id}' not found")
            return pipeline
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving pipeline with ID '{pipeline_id}': {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    async def get_all(self):
        """Retrieves all use_cases."""

        try:
            result = await self.db.execute(select(Pipeline))
            pipelines = result.scalars().all()
            return pipelines
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving all use_cases: {e}")
            raise HTTPException(status_code=500, detail=f"Database error: {e}")


### .options(selectinload(Pipeline.runs)