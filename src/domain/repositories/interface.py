import abc
from typing import Optional, List, TypeVar, Generic

from src.domain.entities.pipeline import PipelineCreateDto
from src.domain.entities.run import RunCreateDto

T = TypeVar('T')  # Define a generic type variable


class BaseRepositoryInterface(Generic[T], abc.ABC):
    """
    Abstract base class defining the repository interface.

    This interface defines the methods that any concrete repository implementation
    must provide.  It uses a generic type variable `T` to represent the type of
    entity being managed (e.g., Pipeline, Run).
    """

    @abc.abstractmethod
    async def create(self, entity: T) -> T:
        """
        Creates a new entity.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """
        Retrieves an entity by its ID.
        """
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self) -> List[T]:
        """
        Retrieves all entities.
        """
        raise NotImplementedError



class PipelineRepositoryInterface(BaseRepositoryInterface[PipelineCreateDto], abc.ABC):
    """
    Specific interface for Pipeline repositories.
    """
    # @abc.abstractmethod
    # async def get_by_name(self, name: str) -> Optional[PipelineCreateDto]:
    #     """
    #     Retrieves a pipeline by its name.
    #     """
    #     raise NotImplementedError


class RunRepositoryInterface(BaseRepositoryInterface[RunCreateDto], abc.ABC):
    """
    Specific interface for Run repositories.
    """

    @abc.abstractmethod
    async def get_all_by_pipeline_id(self, id: int) -> Optional[RunCreateDto]:
        """
        Retrieves a run by the pipeline ID.
        """
        raise NotImplementedError


