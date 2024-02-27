from enum import Enum
from sqlalchemy import Column, Enum as EnumColumn, Integer, String
from app.db.database import Base

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

    id = Column(Integer, primary_key=True)
    name = Column(String)
    foundation = Column(Integer)
    members = Column(Integer)
    nazarenos = Column(Integer)
    description = Column(String)
    colors = Column(String)
    day = Column(EnumColumn(DayEnum))
    her_id = Column(Integer)
