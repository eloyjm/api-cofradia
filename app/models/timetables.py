from sqlalchemy import Column, Enum, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.postgresdb_manager import db_manager
from enum import Enum as PyEnum


class EntityEnum(PyEnum):
    CRUZ = "CRUZ"
    PALIO = "PALIO"


class Timetable(db_manager.base_schemas):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    time = Column(String)  # Use time format
    entity = Column(Enum(EntityEnum), nullable=False)
    hermandad_id = Column(
        Integer, ForeignKey("hermandad.id", ondelete="CASCADE")
    )
    hermandad = relationship("Hermandad", back_populates="timetables")
