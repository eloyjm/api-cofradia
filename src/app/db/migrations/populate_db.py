from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.hermandades import Hermandad 
from ..models.hermandades import DayEnum 
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
    
    #Hermandades del domingo de ramos
    hermandadDR0 = Hermandad(name="El Amor", day=DayEnum.DR, her_id=0)
    db.add(hermandadDR0)
    hermandadDR1 = Hermandad(name="Jesús Despojado", day=DayEnum.DR, her_id=1)
    db.add(hermandadDR1)
    hermandadDR2 = Hermandad(name="La Amargura", day=DayEnum.DR, her_id=2)
    db.add(hermandadDR2)
    hermandadDR3 = Hermandad(name="La Borriquita", day=DayEnum.DR, her_id=3)
    db.add(hermandadDR3)
    hermandadDR4 = Hermandad(name="La Cena", day=DayEnum.DR, her_id=4)
    db.add(hermandadDR4)
    hermandadDR5 = Hermandad(name="La Estrella", day=DayEnum.DR, her_id=5)
    db.add(hermandadDR5)
    hermandadDR6 = Hermandad(name="La Paz", day=DayEnum.DR, her_id=6)
    db.add(hermandadDR6)
    hermandadDR7 = Hermandad(name="San Roque", day=DayEnum.DR, her_id=7)
    db.add(hermandadDR7)


    #Hermandades del lunes
    hermandadLS0 = Hermandad(name="Las Aguas", day=DayEnum.LS, her_id=0)
    db.add(hermandadLS0)
    hermandadLS1 = Hermandad(name="San Gonzalo", day=DayEnum.LS, her_id=1)
    db.add(hermandadLS1)
    hermandadLS2 = Hermandad(name="San Pablo", day=DayEnum.LS, her_id=2)
    db.add(hermandadLS2)
    hermandadLS3 = Hermandad(name="Santa Genovena", day=DayEnum.LS, her_id=3)
    db.add(hermandadLS3)
    hermandadLS4 = Hermandad(name="Santa Marta", day=DayEnum.LS, her_id=4)
    db.add(hermandadLS4)
    hermandadLS5 = Hermandad(name="Vera Cruz", day=DayEnum.LS, her_id=5)
    db.add(hermandadLS5)

    #Hermandades del martes
    hermandadMS0 = Hermandad(name="El Cerro", day=DayEnum.MS, her_id=0)
    db.add(hermandadMS0)
    hermandadMS1 = Hermandad(name="El Dulce Nombre", day=DayEnum.MS, her_id=1)
    db.add(hermandadMS1)
    hermandadMS2 = Hermandad(name="La Candelaria", day=DayEnum.MS, her_id=2)
    db.add(hermandadMS2)
    hermandadMS3 = Hermandad(name="Los Estudiantes", day=DayEnum.MS, her_id=3)
    db.add(hermandadMS3)
    hermandadMS4 = Hermandad(name="Los Javieres", day=DayEnum.MS, her_id=4)
    db.add(hermandadMS4)
    hermandadMS5 = Hermandad(name="San Benito", day=DayEnum.MS, her_id=5)
    db.add(hermandadMS5)
    hermandadMS6 = Hermandad(name="San Esteban", day=DayEnum.MS, her_id=6)
    db.add(hermandadMS6)
    hermandadMS7 = Hermandad(name="Santa Cruz", day=DayEnum.MS, her_id=7)
    db.add(hermandadMS7)

    # Hermandades del miércoles
    hermandadXS0 = Hermandad(name="Cristo de Burgos", day=DayEnum.XS, her_id=0)
    db.add(hermandadXS0)
    hermandadXS1 = Hermandad(name="El Baratillo", day=DayEnum.XS, her_id=1)
    db.add(hermandadXS1)
    hermandadXS2 = Hermandad(name="El Buen Fin", day=DayEnum.XS, her_id=2)
    db.add(hermandadXS2)
    hermandadXS3 = Hermandad(name="La Carmen", day=DayEnum.XS, her_id=3)
    db.add(hermandadXS3)
    hermandadXS4 = Hermandad(name="La Lanzada", day=DayEnum.XS, her_id=4)
    db.add(hermandadXS4)
    hermandadXS5 = Hermandad(name="La Sed", day=DayEnum.XS, her_id=5)
    db.add(hermandadXS5)
    hermandadXS6 = Hermandad(name="Las Siete Palabras", day=DayEnum.XS, her_id=6)
    db.add(hermandadXS6)
    hermandadXS7 = Hermandad(name="Los Panaderos", day=DayEnum.XS, her_id=7)
    db.add(hermandadXS7)
    hermandadXS8 = Hermandad(name="San Bernardo", day=DayEnum.XS, her_id=8)
    db.add(hermandadXS8)

    # Hermandades del jueves
    hermandadJS0 = Hermandad(name="El Valle", day=DayEnum.JS, her_id=0)
    db.add(hermandadJS0)
    hermandadJS1 = Hermandad(name="La Exaltación", day=DayEnum.JS, her_id=1)
    db.add(hermandadJS1)
    hermandadJS2 = Hermandad(name="La Pasión", day=DayEnum.JS, her_id=2)
    db.add(hermandadJS2)
    hermandadJS3 = Hermandad(name="La Quinta Angustia", day=DayEnum.JS, her_id=3)
    db.add(hermandadJS3)
    hermandadJS4 = Hermandad(name="Las Cigarreras", day=DayEnum.JS, her_id=4)
    db.add(hermandadJS4)
    hermandadJS5 = Hermandad(name="Los Negritos", day=DayEnum.JS, her_id=5)
    db.add(hermandadJS5)
    hermandadJS6 = Hermandad(name="Montesión", day=DayEnum.JS, her_id=6)
    db.add(hermandadJS6)

    # Hermandades de la madrugá
    hermandadM0 = Hermandad(name="El Calvario", day=DayEnum.M, her_id=0) 
    db.add(hermandadM0) 
    hermandadM1 = Hermandad(name="El Gran Poder", day=DayEnum.M, her_id=1) 
    db.add(hermandadM1) 
    hermandadM2 = Hermandad(name="El Silencio", day=DayEnum.M, her_id=2) 
    db.add(hermandadM2) 
    hermandadM3 = Hermandad(name="La Esperanza de Triana", day=DayEnum.M, her_id=3) 
    db.add(hermandadM3) 
    hermandadM4 = Hermandad(name="La Macarena", day=DayEnum.M, her_id=4) 
    db.add(hermandadM4) 
    hermandadM5 = Hermandad(name="Los Gitanos", day=DayEnum.M, her_id=5) 
    db.add(hermandadM5)

    # Hermandades del viernes
    hermandadVS0 = Hermandad(name="El Cachorro", day=DayEnum.VS, her_id=0)
    db.add(hermandadVS0)
    hermandadVS1 = Hermandad(name="La Carretería", day=DayEnum.VS, her_id=1)
    db.add(hermandadVS1)
    hermandadVS2 = Hermandad(name="La O", day=DayEnum.VS, her_id=2)
    db.add(hermandadVS2)
    hermandadVS3 = Hermandad(name="La Sagrada Mortaja", day=DayEnum.VS, her_id=3)
    db.add(hermandadVS3)
    hermandadVS4 = Hermandad(name="La Soledad de San Buenaventura", day=DayEnum.VS, her_id=4)
    db.add(hermandadVS4)
    hermandadVS5 = Hermandad(name="Montserrat", day=DayEnum.VS, her_id=5)
    db.add(hermandadVS5)
    hermandadVS6 = Hermandad(name="San Isidoro", day=DayEnum.VS, her_id=6)
    db.add(hermandadVS6)

    # Hermandades del sábado
    hermandadSS0 = Hermandad(name="El Santo Entierro", day=DayEnum.SS, her_id=0)
    db.add(hermandadSS0)
    hermandadSS1 = Hermandad(name="El Sol", day=DayEnum.SS, her_id=1)
    db.add(hermandadSS1)
    hermandadSS2 = Hermandad(name="La Soledad De San Lorenzo", day=DayEnum.SS, her_id=2)
    db.add(hermandadSS2)
    hermandadSS3 = Hermandad(name="La Trinidad", day=DayEnum.SS, her_id=3)
    db.add(hermandadSS3)
    hermandadSS4 = Hermandad(name="Los Servitas", day=DayEnum.SS, her_id=4)
    db.add(hermandadSS4)

    # Hermandades del domingo de resurreción
    hermandadDDR0 = Hermandad(name="La Resurrección", day=DayEnum.DDR, her_id=0)
    db.add(hermandadDDR0)

    db.commit()

    


