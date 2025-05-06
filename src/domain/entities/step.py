from pydantic import BaseModel


class Step(BaseModel):
    name: str
    description: str
    location: str
    parameters: str

