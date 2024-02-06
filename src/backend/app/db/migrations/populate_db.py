from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models.hermandades import Hermandad 
from app.db.models.hermandades import DayEnum 
import os
from dotenv import load_dotenv

 
###CONEXION CON LA BASE DE DATOS
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)

def populate_database():
    db = SessionLocal()
    db.query(Hermandad).delete()
    db.commit()

    #Hermandades del lunes
    hermandad0 = Hermandad(name="Las Aguas", day=DayEnum.LS, her_id=0)
    db.add(hermandad0)
    hermandad1 = Hermandad(name="San Gonzalo", day=DayEnum.LS, her_id=1)
    db.add(hermandad1)
    hermandad2 = Hermandad(name="San Pablo", day=DayEnum.LS, her_id=2)
    db.add(hermandad2)
    hermandad3 = Hermandad(name="Santa Genovena", day=DayEnum.LS, her_id=3)
    db.add(hermandad3)
    hermandad4 = Hermandad(name="Santa Marta", day=DayEnum.LS, her_id=4)
    db.add(hermandad4)
    hermandad5 = Hermandad(name="Vera Cruz", day=DayEnum.LS, her_id=5)
    db.add(hermandad5)

    db.commit()

    


