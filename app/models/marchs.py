from sqlalchemy import Column, String, Integer
from database.postgresdb_manager import db_manager


class March(db_manager.base_schemas):
    __tablename__ = "march"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    author = Column(String)
    description = Column(String)
    url = Column(String)
