from pydantic import BaseModel
from typing import Optional, List


class RunCreateRequest(BaseModel):
    status: Optional[str] = "Pending"
    metadata_: Optional[str] = None

class RunCreateDto(RunCreateRequest):
    pipeline_id: int

class RunDto(RunCreateDto):
    id: int

    class Config:
        from_attributes = True

class RunResponse(BaseModel):
    pipeline_id: int
    runs: List[RunDto]