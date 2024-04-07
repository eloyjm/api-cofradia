from sqlalchemy import Column, Enum, Time, String, ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class TimeTable(Base):
    __tablename__ = 'timetables'
    id = Column(String, primary_key=True)
    location = Column(String)
    time = Column(Time)
    entity = Column(Enum("CRUZ", "PALIO", name="entity_enum"), nullable=False)
    
    hermandad_id = Column(String, ForeignKey('hermandades.id', ondelete='CASCADE'))
    hermandad = relationship("Hermandad", back_populates="timetables")

