from pydantic import BaseModel
from typing import List, Optional

from src.domain.entities.run import RunDto


class PipelineBase(BaseModel):
    name: str
    description: str
    workflow: Optional[str]

class PipelineCreateDto(PipelineBase):
    pass

class PipelineDto(PipelineBase):
    id: int
    # runs: List["RunDto"] = []

    class Config:
        from_attributes = True