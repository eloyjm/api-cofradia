from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from ..db.models.timetables import TimeTable as DBTimeTable
from sqlalchemy.orm import Session
from typing import Annotated
from ..db.database import get_db
from ..schemas.timetables import TimeTable
from ..db.models.hermandades import Hermandad as DBHermandad
import uuid
from datetime import datetime

timetables_router = APIRouter(tags=["timetables"])
db_dependency = Annotated[Session, Depends(get_db)]

@timetables_router.get('/timetables', status_code=status.HTTP_200_OK)
def get_timetables(db: db_dependency):
    try:
        timetables = db.query(DBTimeTable).all()
        return timetables
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    

@timetables_router.get('/timetables/list/{id}', status_code=status.HTTP_200_OK)
def get_timetables_by_id(db: db_dependency, id: str):
    try:
        timetable = db.query(DBTimeTable).filter(DBTimeTable.id == id).first()
        return timetable
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@timetables_router.get('/timetables/hermandades/{her_id}', status_code=status.HTTP_200_OK)
def get_timetables_by_hermandad(db: db_dependency, her_id: str):
    try:
        timetables = db.query(DBTimeTable).filter(DBTimeTable.hermandad_id == her_id).all()
        return timetables
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@timetables_router.post('/timetables/new', status_code=status.HTTP_200_OK)
def create_timetable(db: db_dependency, timetable_data : TimeTable):
    try:
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == timetable_data.hermandad_id).first()
        if not hermandad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Hermandad no encontrada")
        
        time = datetime.strptime(timetable_data.time, '%H:%M').time()
        if not time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Formato de hora incorrecto")
        
        new_timetable = DBTimeTable(id = str(uuid.uuid4()), time=time,entity=timetable_data.entity.name, **timetable_data.model_dump(exclude={"time", "entity"}))
        db.add(new_timetable)

        db.commit()
        db.refresh(new_timetable)
        return new_timetable
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")