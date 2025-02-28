from sqlalchemy import Column, Enum, Time, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from database.postgresdb_manager import db_manager


class Timetable(db_manager.base_schemas):
    __tablename__ = "timetable"
    id = Column(Integer, primary_key=True, autoincrement=True)
    location = Column(String)
    time = Column(Time)
    entity = Column(Enum("CRUZ", "PALIO", name="entity_enum"), nullable=False)
    hermandad_id = Column(
        Integer, ForeignKey("hermandad.id", ondelete="CASCADE")
    )
    hermandad = relationship("Hermandad", back_populates="timetables")
