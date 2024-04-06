from pydantic import BaseModel
from enum import Enum as PyEnum

class EntityEnum(PyEnum):
    CRUZ = 'Cruz'
    PALIO = 'Palio'

class TimeTable(BaseModel):
    location : str
    time : str
    entity : EntityEnum
    hermandad_id : str