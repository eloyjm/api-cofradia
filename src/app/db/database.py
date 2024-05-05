from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from ...config import Config
from dotenv import load_dotenv
 
###CONEXION CON LA BASE DE DATOS
load_dotenv()

engine = create_engine(Config.get_database_url())
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)
Base = declarative_base()
 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()