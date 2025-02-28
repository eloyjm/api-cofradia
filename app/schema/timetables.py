from pydantic import BaseModel
from models.timetables import EntityEnum


class TimetableSchema(BaseModel):
    location: str
    time: str
    entity: EntityEnum
    hermandad_id: int
