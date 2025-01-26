from sqlalchemy import Column, String
from database.postgresdb_manager import db_manager


class Marchas(db_manager.base_schemas):
    __tablename__ = 'marchas'
    id = Column(String, primary_key=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    url = Column(String)
