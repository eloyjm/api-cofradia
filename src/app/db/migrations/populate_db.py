from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models.hermandades import Hermandad 
from ..models.hermandades import DayEnum 
import os
from dotenv import load_dotenv
import uuid

 
###CONEXION CON LA BASE DE DATOS
load_dotenv()
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 
SessionLocal = sessionmaker(bind=engine, autocommit = False, autoflush = False)

def populate_database():
    db = SessionLocal()
    db.query(Hermandad).delete()
    
    #Hermandades del domingo de ramos
    hermandadDR0 = Hermandad(id=str(uuid.uuid4()), name="El Amor", day=DayEnum.DR, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Amor_(Sevilla)")
    db.add(hermandadDR0)
    hermandadDR1 = Hermandad(id=str(uuid.uuid4()), name="Jesús Despojado", day=DayEnum.DR, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Jes%C3%BAs_Despojado_(Sevilla)")
    db.add(hermandadDR1)
    hermandadDR2 = Hermandad(id=str(uuid.uuid4()), name="La Amargura", day=DayEnum.DR, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Amargura_(Sevilla)")
    db.add(hermandadDR2)
    hermandadDR3 = Hermandad(id=str(uuid.uuid4()), name="La Borriquita", day=DayEnum.DR, her_id=3, wiki_url="")
    db.add(hermandadDR3)
    hermandadDR4 = Hermandad(id=str(uuid.uuid4()), name="La Cena", day=DayEnum.DR, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Cena_(Sevilla)")
    db.add(hermandadDR4)
    hermandadDR5 = Hermandad(id=str(uuid.uuid4()), name="La Estrella", day=DayEnum.DR, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Estrella_(Sevilla)")
    db.add(hermandadDR5)
    hermandadDR6 = Hermandad(id=str(uuid.uuid4()), name="La Hiniesta", day=DayEnum.DR, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Hiniesta_(Sevilla)")
    db.add(hermandadDR6)
    hermandadDR7 = Hermandad(id=str(uuid.uuid4()), name="La Paz", day=DayEnum.DR, her_id=7, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Paz_(Sevilla)")
    db.add(hermandadDR7)
    hermandadDR8 = Hermandad(id=str(uuid.uuid4()), name="San Roque", day=DayEnum.DR, her_id=8, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Roque_(Sevilla)")
    db.add(hermandadDR8)


    #Hermandades del lunes
    hermandadLS0 = Hermandad(id=str(uuid.uuid4()), name="El Museo", day=DayEnum.LS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Museo_(Sevilla)")
    db.add(hermandadLS0)
    hermandadLS1 = Hermandad(id=str(uuid.uuid4()), name="La Redención", day=DayEnum.LS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Redenci%C3%B3n_(Sevilla)")
    db.add(hermandadLS1)
    hermandadLS2 = Hermandad(id=str(uuid.uuid4()), name="Las Aguas", day=DayEnum.LS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_las_Aguas_(Sevilla)")
    db.add(hermandadLS2)
    hermandadLS3 = Hermandad(id=str(uuid.uuid4()), name="Las Penas", day=DayEnum.LS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_las_Penas_(Sevilla)")
    db.add(hermandadLS3)
    hermandadLS4 = Hermandad(id=str(uuid.uuid4()), name="San Gonzalo", day=DayEnum.LS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Gonzalo_(Sevilla)")
    db.add(hermandadLS4)
    hermandadLS5 = Hermandad(id=str(uuid.uuid4()), name="San Pablo", day=DayEnum.LS, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Pablo_(Sevilla)")
    db.add(hermandadLS5)
    hermandadLS6 = Hermandad(id=str(uuid.uuid4()), name="Santa Genovena", day=DayEnum.LS, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Santa_Genoveva_(Sevilla)")
    db.add(hermandadLS6)
    hermandadLS7 = Hermandad(id=str(uuid.uuid4()), name="Santa Marta", day=DayEnum.LS, her_id=7, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Santa_Marta_(Sevilla)")
    db.add(hermandadLS7)
    hermandadLS8 = Hermandad(id=str(uuid.uuid4()), name="Vera Cruz", day=DayEnum.LS, her_id=8, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Vera_Cruz_(Sevilla)")
    db.add(hermandadLS8)

    #Hermandades del martes
    hermandadMS0 = Hermandad(id=str(uuid.uuid4()), name="El Cerro", day=DayEnum.MS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Cerro_(Sevilla)")
    db.add(hermandadMS0)
    hermandadMS1 = Hermandad(id=str(uuid.uuid4()), name="El Dulce Nombre", day=DayEnum.MS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Dulce_Nombre_(Sevilla)")
    db.add(hermandadMS1)
    hermandadMS2 = Hermandad(id=str(uuid.uuid4()), name="La Candelaria", day=DayEnum.MS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Candelaria_(Sevilla)")
    db.add(hermandadMS2)
    hermandadMS3 = Hermandad(id=str(uuid.uuid4()), name="Los Estudiantes", day=DayEnum.MS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Estudiantes_(Sevilla)")
    db.add(hermandadMS3)
    hermandadMS4 = Hermandad(id=str(uuid.uuid4()), name="Los Javieres", day=DayEnum.MS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Javieres_(Sevilla)")
    db.add(hermandadMS4)
    hermandadMS5 = Hermandad(id=str(uuid.uuid4()), name="San Benito", day=DayEnum.MS, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Benito_(Sevilla)")
    db.add(hermandadMS5)
    hermandadMS6 = Hermandad(id=str(uuid.uuid4()), name="San Esteban", day=DayEnum.MS, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Esteban_(Sevilla)")
    db.add(hermandadMS6)
    hermandadMS7 = Hermandad(id=str(uuid.uuid4()), name="Santa Cruz", day=DayEnum.MS, her_id=7, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Santa_Cruz_(Sevilla)")
    db.add(hermandadMS7)

    # Hermandades del miércoles
    hermandadXS0 = Hermandad(id=str(uuid.uuid4()), name="Cristo de Burgos", day=DayEnum.XS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Cristo_de_Burgos_(Sevilla)")
    db.add(hermandadXS0)
    hermandadXS1 = Hermandad(id=str(uuid.uuid4()), name="El Baratillo", day=DayEnum.XS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Baratillo_(Sevilla)")
    db.add(hermandadXS1)
    hermandadXS2 = Hermandad(id=str(uuid.uuid4()), name="El Buen Fin", day=DayEnum.XS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Buen_Fin_(Sevilla)")
    db.add(hermandadXS2)
    hermandadXS3 = Hermandad(id=str(uuid.uuid4()), name="El Carmen", day=DayEnum.XS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Carmen_(Sevilla)")
    db.add(hermandadXS3)
    hermandadXS4 = Hermandad(id=str(uuid.uuid4()), name="La Lanzada", day=DayEnum.XS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Lanzada_(Sevilla)")
    db.add(hermandadXS4)
    hermandadXS5 = Hermandad(id=str(uuid.uuid4()), name="La Sed", day=DayEnum.XS, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Sed_(Sevilla)")
    db.add(hermandadXS5)
    hermandadXS6 = Hermandad(id=str(uuid.uuid4()), name="Las Siete Palabras", day=DayEnum.XS, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_las_Siete_Palabras_(Sevilla)")
    db.add(hermandadXS6)
    hermandadXS7 = Hermandad(id=str(uuid.uuid4()), name="Los Panaderos", day=DayEnum.XS, her_id=7, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Panaderos_(Sevilla)")
    db.add(hermandadXS7)
    hermandadXS8 = Hermandad(id=str(uuid.uuid4()), name="San Bernardo", day=DayEnum.XS, her_id=8, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_San_Bernardo_(Sevilla)")
    db.add(hermandadXS8)

    # Hermandades del jueves
    hermandadJS0 = Hermandad(id=str(uuid.uuid4()), name="El Valle", day=DayEnum.JS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Valle_(Sevilla)")
    db.add(hermandadJS0)
    hermandadJS1 = Hermandad(id=str(uuid.uuid4()), name="La Exaltación", day=DayEnum.JS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Exaltaci%C3%B3n_(Sevilla)")
    db.add(hermandadJS1)
    hermandadJS2 = Hermandad(id=str(uuid.uuid4()), name="La Pasión", day=DayEnum.JS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Pasi%C3%B3n_(Sevilla)")
    db.add(hermandadJS2)
    hermandadJS3 = Hermandad(id=str(uuid.uuid4()), name="La Quinta Angustia", day=DayEnum.JS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Quinta_Angustia_(Sevilla)")
    db.add(hermandadJS3)
    hermandadJS4 = Hermandad(id=str(uuid.uuid4()), name="Las Cigarreras", day=DayEnum.JS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_las_Cigarreras_(Sevilla)")
    db.add(hermandadJS4)
    hermandadJS5 = Hermandad(id=str(uuid.uuid4()), name="Los Negritos", day=DayEnum.JS, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Negritos_(Sevilla)")
    db.add(hermandadJS5)
    hermandadJS6 = Hermandad(id=str(uuid.uuid4()), name="Montesión", day=DayEnum.JS, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Monte-Sion")
    db.add(hermandadJS6)

    # Hermandades de la madrugá
    hermandadM0 = Hermandad(id=str(uuid.uuid4()), name="El Calvario", day=DayEnum.M, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Calvario_(Sevilla)") 
    db.add(hermandadM0) 
    hermandadM1 = Hermandad(id=str(uuid.uuid4()), name="El Gran Poder", day=DayEnum.M, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Jes%C3%BAs_del_Gran_Poder") 
    db.add(hermandadM1) 
    hermandadM2 = Hermandad(id=str(uuid.uuid4()), name="El Silencio", day=DayEnum.M, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Silencio_(Sevilla)") 
    db.add(hermandadM2) 
    hermandadM3 = Hermandad(id=str(uuid.uuid4()), name="La Esperanza de Triana", day=DayEnum.M, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Esperanza_de_Triana") 
    db.add(hermandadM3) 
    hermandadM4 = Hermandad(id=str(uuid.uuid4()), name="La Macarena", day=DayEnum.M, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Macarena_(Sevilla)") 
    db.add(hermandadM4) 
    hermandadM5 = Hermandad(id=str(uuid.uuid4()), name="Los Gitanos", day=DayEnum.M, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Gitanos_(Sevilla)") 
    db.add(hermandadM5)

    # Hermandades del viernes
    hermandadVS0 = Hermandad(id=str(uuid.uuid4()), name="El Cachorro", day=DayEnum.VS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Cachorro_(Sevilla)")
    db.add(hermandadVS0)
    hermandadVS1 = Hermandad(id=str(uuid.uuid4()), name="La Carretería", day=DayEnum.VS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Carreter%C3%ADa_(Sevilla)")
    db.add(hermandadVS1)
    hermandadVS2 = Hermandad(id=str(uuid.uuid4()), name="La O", day=DayEnum.VS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_O_(Sevilla)")
    db.add(hermandadVS2)
    hermandadVS3 = Hermandad(id=str(uuid.uuid4()), name="La Sagrada Mortaja", day=DayEnum.VS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Sagrada_Mortaja_(Sevilla)")
    db.add(hermandadVS3)
    hermandadVS4 = Hermandad(id=str(uuid.uuid4()), name="La Soledad de San Buenaventura", day=DayEnum.VS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Soledad_de_San_Buenaventura_(Sevilla)")
    db.add(hermandadVS4)
    hermandadVS5 = Hermandad(id=str(uuid.uuid4()), name="Montserrat", day=DayEnum.VS, her_id=5, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_Montserrat_(Sevilla)")
    db.add(hermandadVS5)
    hermandadVS6 = Hermandad(id=str(uuid.uuid4()), name="Las Tres Caídas", day=DayEnum.VS, her_id=6, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_las_Tres_Ca%C3%ADdas_(Sevilla)")
    db.add(hermandadVS6)

    # Hermandades del sábado
    hermandadSS0 = Hermandad(id=str(uuid.uuid4()), name="El Santo Entierro", day=DayEnum.SS, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Santo_Entierro_(Sevilla)")
    db.add(hermandadSS0)
    hermandadSS1 = Hermandad(id=str(uuid.uuid4()), name="El Sol", day=DayEnum.SS, her_id=1, wiki_url="https://es.wikipedia.org/wiki/Hermandad_del_Sol_(Sevilla)")
    db.add(hermandadSS1)
    hermandadSS2 = Hermandad(id=str(uuid.uuid4()), name="La Soledad De San Lorenzo", day=DayEnum.SS, her_id=2, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Soledad_de_San_Lorenzo_(Sevilla)")
    db.add(hermandadSS2)
    hermandadSS3 = Hermandad(id=str(uuid.uuid4()), name="La Trinidad", day=DayEnum.SS, her_id=3, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Trinidad_(Sevilla)")
    db.add(hermandadSS3)
    hermandadSS4 = Hermandad(id=str(uuid.uuid4()), name="Los Servitas", day=DayEnum.SS, her_id=4, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_los_Servitas_(Sevilla)")
    db.add(hermandadSS4)

    # Hermandades del domingo de resurreción
    hermandadDDR0 = Hermandad(id=str(uuid.uuid4()), name="La Resurrección", day=DayEnum.DDR, her_id=0, wiki_url="https://es.wikipedia.org/wiki/Hermandad_de_la_Resurrecci%C3%B3n_(Sevilla)")
    db.add(hermandadDDR0)

    db.commit()

    


