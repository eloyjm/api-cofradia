from enum import Enum
from sqlalchemy import Column, Enum as EnumColumn, Time, String, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class EntityEnum(Enum):
    CRUZ = 'Cruz'
    PALIO = 'Palio'

class TimeTable(Base):
    __tablename__ = 'timetables'
    id = Column(String, primary_key=True)
    location = Column(String)
    time = Column(Time)
    entity = Column(EnumColumn(EntityEnum))
    
    hermandad_id = Column(String, ForeignKey('hermandades.id', ondelete='CASCADE'))
    hermandad = relationship("Hermandad", back_populates="timetables")

