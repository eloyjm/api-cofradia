from enum import Enum
from sqlalchemy import Column, Enum as EnumColumn, Integer, String
from ..database import Base
from sqlalchemy.orm import relationship
from .timetables import TimeTable

class DayEnum(Enum):
    DR = 'Domingo de Ramos'
    LS = 'Lunes Santo'
    MS = 'Martes Santo'
    XS = 'Miércoles Santo'
    JS = 'Jueves Santo'
    M = 'Madrugá'
    VS = 'Viernes Santo'
    SS = 'Sábado Santo'
    DDR = 'Domingo de Resurrección'

class Hermandad(Base):
    __tablename__ = 'hermandades'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String)
    foundation = Column(String)
    members = Column(String)
    nazarenos = Column(String)
    history = Column(String)
    passages_number = Column(String)
    location = Column(String)
    colors = Column(String)
    color_one = Column(String)
    color_two = Column(String)
    day_time = Column(String)
    canonical_seat = Column(String)
    day = Column(EnumColumn(DayEnum))
    wiki_url = Column(String)
    route_url = Column(String)
    escudo_url = Column(String)
    traje_url = Column(String)

    timetables = relationship("TimeTable", back_populates="hermandad")
