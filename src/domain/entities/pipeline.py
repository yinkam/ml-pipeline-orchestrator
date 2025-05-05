from pydantic import BaseModel
from typing import List

from src.domain.entities.run import RunDto


class PipelineBase(BaseModel):
    name: str
    description: str
    workflow: str

class PipelineCreateDto(PipelineBase):
    pass

class PipelineDto(PipelineBase):
    id: int
    # runs: List["RunDto"] = []

    class Config:
        from_attributes = True