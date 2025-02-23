from typing import Optional

import pydantic


class CreateActorRequest(pydantic.BaseModel):
    first_name: str
    last_name: str


class ReadActorResponse(pydantic.BaseModel):
    actor_id: int
    first_name: str
    last_name: str


class UpdateActorRequest(pydantic.BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class DeleteActorResponse(pydantic.BaseModel):
    actor_id: int
