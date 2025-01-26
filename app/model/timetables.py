from sqlalchemy import Column, Enum, Time, String, ForeignKey
from sqlalchemy.orm import relationship
from database.postgresdb_manager import db_manager


class TimeTable(db_manager.base_schemas):
    __tablename__ = 'timetables'
    id = Column(String, primary_key=True)
    location = Column(String)
    time = Column(Time)
    entity = Column(Enum("CRUZ", "PALIO", name="entity_enum"), nullable=False)
    hermandad_id = Column(
        String, ForeignKey('hermandades.id', ondelete='CASCADE')
    )
    hermandad = relationship("Hermandad", back_populates="timetables")
