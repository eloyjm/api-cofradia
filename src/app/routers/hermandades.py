from fastapi import APIRouter, Depends, status, HTTPException
from app.db.models.hermandades import Hermandad as DBHermandad
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import get_db

hermandades_router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]


@hermandades_router.get('/hermandades', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandades(db: db_dependency):
    try:
        hermandades = db.query(DBHermandad).all()
        return hermandades
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

