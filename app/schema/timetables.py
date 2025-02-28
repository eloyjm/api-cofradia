from pydantic import BaseModel
from enum import Enum as PyEnum


class EntityEnum(PyEnum):
    CRUZ = "CRUZ"
    PALIO = "PALIO"


class TimetableSchema(BaseModel):
    location: str
    time: str
    entity: EntityEnum
    hermandad_id: int
