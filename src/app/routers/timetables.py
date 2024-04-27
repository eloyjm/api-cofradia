from fastapi import APIRouter, Depends, status, HTTPException
from ..db.models.timetables import TimeTable as DBTimeTable
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from ..db.database import get_db
from ..schemas.timetables import TimeTable
from ..db.models.hermandades import Hermandad as DBHermandad
from ..db.models.hermandades import DayEnum
import uuid,re
from datetime import datetime
from ..routers.oauth import  get_current_user
from ..schemas import users
from ..db.migrations.scraping import extract_data_dds
from unidecode import unidecode

timetables_router = APIRouter(tags=["timetables"], prefix="/timetables")
db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[users.User, Depends(get_current_user)]
name_mapping = {
            "la-pasion": "pasion",
            "la-sagrada-mortaja": "la-mortaja",
            "las-tres-caidas": "san-isidoro",
            "la-soledad-de-san-lorenzo": "soledad-de-san-lorenzo",
            "el-dulce-nombre": "dulce-nombre",
            "san-pablo": "el-poligono-de-san-pablo",
            "cristo-de-burgos": "el-cristo-de-burgos",
            "la-esperanza-de-triana": "esperanza-de-triana",
        }

@timetables_router.get('/', status_code=status.HTTP_200_OK)
def get_timetables(db: db_dependency):
    try:
        timetables = db.query(DBTimeTable).all()
        return timetables
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    

@timetables_router.get('/list/{id}', status_code=status.HTTP_200_OK)
def get_timetables_by_id(db: db_dependency, id: str):
    try:
        timetable = db.query(DBTimeTable).filter(DBTimeTable.id == id).first()
        return timetable
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@timetables_router.get('/hermandades/{her_id}', status_code=status.HTTP_200_OK)
def get_timetables_by_hermandad(db: db_dependency, her_id: str):
    try:
        timetables = db.query(DBTimeTable).filter(DBTimeTable.hermandad_id == her_id).all()
        return timetables
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@timetables_router.post('/new', status_code=status.HTTP_200_OK)
def create_timetable(db: db_dependency, timetable_data : TimeTable, current_user:current_user):
    try:
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == timetable_data.hermandad_id).first()
        if not hermandad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hermandad no encontrada")
        
        time = datetime.strptime(timetable_data.time, '%H:%M').time()
        if not time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de hora incorrecto")
        
        new_timetable = DBTimeTable(id = str(uuid.uuid4()), time=time, entity=timetable_data.entity.name, **timetable_data.model_dump(exclude={"time", "entity"}))
        db.add(new_timetable)

        db.commit()
        db.refresh(new_timetable)
        return new_timetable
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@timetables_router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_timetable(db: db_dependency, id: str, current_user:current_user):
    try:
        timetable = db.query(DBTimeTable).filter(DBTimeTable.id == id).first()
        if not timetable:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Timetable not found")
        
        db.delete(timetable)
        db.commit()
        
        return {"detail": "Timetable deleted successfully"}
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error:{str(e)}")
    
@timetables_router.post('/migrate/all', status_code=status.HTTP_200_OK)
async def migrate_timetables(db: db_dependency, current_user:current_user):
    try:
        db.query(DBTimeTable).delete()
        db.commit()
        
        hermandades = db.query(DBHermandad).all()
        for hermandad in hermandades:
            name = unidecode(hermandad.name.lower().replace(" ", "-"))
            
            name = name_mapping.get(name, name)

            url = f"https://www.diariodesevilla.es/contenidos/programa-semana-santa-sevilla/{name}.php"
            data, map_src = extract_data_dds(url)
            if map_src:
                hermandad.route_url = map_src
            for row in data:
                time = row[1]
                location = row[2]
                match = re.search(r'\((.*?)\)', location)
                if match:
                    time = match.group(1)
                    location = re.sub(r'\(.*?\)', '', location)

                if time != "":
                    time = datetime.strptime(time.replace(".", ":"), '%H:%M').time()
                    if not time:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de hora incorrecto")
                    new_timetable = DBTimeTable(id = str(uuid.uuid4()), time=time, entity=row[0], location=location, hermandad=hermandad)
                    db.add(new_timetable)

        db.commit()
        return {"message": "Datos actualizados"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@timetables_router.post('/migrate/day/{day}', status_code=status.HTTP_200_OK)
async def migrate_timetables(db: db_dependency, day: DayEnum, current_user:current_user):
    try:
        hermandades = db.query(DBHermandad).filter(DBHermandad.day == day).all()
        
        her_ids = [her.id for her in hermandades]
        db.query(DBTimeTable).filter(DBTimeTable.hermandad_id.in_(her_ids)).delete()

        db.commit()

        for hermandad in hermandades:
            name = unidecode(hermandad.name.lower().replace(" ", "-"))
            
            name = name_mapping.get(name, name)

            url = f"https://www.diariodesevilla.es/contenidos/programa-semana-santa-sevilla/{name}.php"
            data, map_src = extract_data_dds(url)
            if map_src:
                hermandad.route_url = map_src

            for row in data:
                time = row[1]
                location = row[2]
                match = re.search(r'\((.*?)\)', location)
                if match:
                    time = match.group(1)
                    location = re.sub(r'\(.*?\)', '', location)

                if time != "":
                    time = datetime.strptime(time.replace(".", ":"), '%H:%M').time()
                    if not time:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de hora incorrecto")
                    new_timetable = DBTimeTable(id = str(uuid.uuid4()), time=time, entity=row[0], location=location, hermandad=hermandad)
                    db.add(new_timetable)

        db.commit()
        return {"message": "Datos actualizados"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@timetables_router.post('/migrate/{her_id}', status_code=status.HTTP_200_OK)
async def migrate_timetables_by_id(db: db_dependency, her_id: str, current_user:current_user):
    try:
        db.query(DBTimeTable).filter(DBTimeTable.hermandad_id == her_id).delete()
        db.commit()
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == her_id).first()
        if not hermandad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hermandad not found")
        
        name = unidecode(hermandad.name.lower().replace(" ", "-"))
        name = name_mapping.get(name, name)

        url = f"https://www.diariodesevilla.es/contenidos/programa-semana-santa-sevilla/{name}.php"
        data, map_src = extract_data_dds(url)
        if map_src:
                hermandad.route_url = map_src
        for row in data:
                time = row[1]
                location = row[2]
                match = re.search(r'\((.*?)\)', location)
                if match:
                    time = match.group(1)
                    location = re.sub(r'\(.*?\)', '', location)

                if time != "":
                    time = datetime.strptime(time.replace(".", ":"), '%H:%M').time()
                    if not time:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de hora incorrecto")
                    new_timetable = DBTimeTable(id = str(uuid.uuid4()), time=time, entity=row[0], location=location, hermandad=hermandad)
                    db.add(new_timetable)
        
        db.commit()
        return {"message": "Datos actualizados"}

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")