from pydantic import BaseModel


class BuildRequest(BaseModel):
    build: str


class BuildResponse(BaseModel):
    tasks: list