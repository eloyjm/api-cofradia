from enum import Enum
from sqlalchemy import Column, Enum as EnumColumn, Integer, String
from app.db.database import Base

class DayEnum(Enum):
    DR = 'Domingo de resurección'
    LS = 'Lunes Santo'
    MS = 'Martes Santo'
    XS = 'Miércoles Santo'
    JS = 'Jueves Santo'
    VS = 'Viernes Santo'
    SS = 'Sábado Santo'
    D = 'Domingo de Resurección'

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
