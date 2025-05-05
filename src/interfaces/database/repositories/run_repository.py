import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from typing import Annotated, Sequence

from src.domain.repositories.interface import RunRepositoryInterface
from src.interfaces.database.core import get_async_db
from src.interfaces.database.models.run import Run
from src.domain.entities.run import RunCreateDto


logger = logging.getLogger(__name__)


class RunRepository(RunRepositoryInterface):

    def __init__(self, db: Annotated[AsyncSession, Depends(get_async_db)]):
        self.db = db

    async def create(self, data: RunCreateDto):
        """
        Repository to create a new pipeline run.
        """
        db_run = Run(**data.model_dump())
        self.db.add(db_run)

        try:
            await self.db.commit()
            await self.db.refresh(db_run)
            logger.info(f"Run created with ID: {db_run.id}")

            return db_run
        except SQLAlchemyError as e:
            await self.db.rollback()
            logger.error(f"Error creating run: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    async def get_by_id(self, run_id):
        """
        Endpoint to list all use_cases.
        """

        try:
            result = await self.db.execute(select(Run).filter_by(id=run_id))
            run = result.scalar_one_or_none()

            return run
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    async def get_all(self):
        """
        Retrieve all runs
        """
        try:
            result = await self.db.execute(select(Run))
            runs = result.scalars().all()

            return runs
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

    async def get_all_by_pipeline_id(self, pipeline_id: int) -> Sequence[Run]:
        """
        Retrieves all runs for a given pipeline ID.
        """
        try:
            result = await self.db.execute(select(Run).filter_by(pipeline_id=pipeline_id))
            runs = result.scalars().all()
            return runs
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving runs for pipeline ID {pipeline_id}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")

