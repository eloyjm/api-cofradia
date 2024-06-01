from sqlalchemy import Column, String
from ..database import Base

class Marchas(Base):
    __tablename__ = 'marchas'
    id = Column(String, primary_key=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    url = Column(String)
    

