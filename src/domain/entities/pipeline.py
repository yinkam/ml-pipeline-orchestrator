from pydantic import BaseModel
from typing import List, Optional, Dict

from src.domain.entities.run import RunDto
from src.domain.entities.step import Step


class PipelineBase(BaseModel):
    name: str
    description: str
    workflow: Dict[str, List[str]] # Step and Dependencies represented as an adjacency list (DAG)
    step_configs: Dict[str, Step] # Store configs of each step


class PipelineCreateDto(PipelineBase):
    pass


class PipelineDto(PipelineBase):
    id: int
    # runs: List["RunDto"] = []

    class Config:
        from_attributes = True