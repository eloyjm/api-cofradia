from fastapi import APIRouter, Depends, status, HTTPException
from ..db.models.marchas import Marchas as DBMarcha
from sqlalchemy.orm import Session, joinedload
from typing import Annotated
from ..db.database import get_db
from ..schemas.marchas import Marcha
import uuid,re
from datetime import datetime
from ..routers.oauth import  get_current_user
from ..schemas import users
from ..db.migrations.scraping import extract_data_marcha
from unidecode import unidecode

marchas_router = APIRouter(tags=["marchas"], prefix="/marchas")
db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[users.User, Depends(get_current_user)]


@marchas_router.get('/', status_code=status.HTTP_200_OK)
def get_marchas(db: db_dependency):
    try:
        marchas = db.query(DBMarcha).all()
        return marchas
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@marchas_router.get('/list/{id}', status_code=status.HTTP_200_OK)
def get_marcha(id: str, db: db_dependency):
    try:
        marcha = db.query(DBMarcha).filter(DBMarcha.id == id).first()
        if not marcha:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcha no encontrada")
        return marcha
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@marchas_router.post('/new', status_code=status.HTTP_201_CREATED)
def create_marcha(marcha: Marcha, db: db_dependency, current_user:current_user):
    try:
        marcha_db = DBMarcha(id=str(uuid.uuid4()), name=marcha.name, author=marcha.author, description=marcha.description, url=marcha.url)
        db.add(marcha_db)
        db.commit()
        return marcha_db
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    

@marchas_router.delete('/delete/{id}', status_code=status.HTTP_200_OK)
def delete_marcha(id: str, db: db_dependency, current_user:current_user):
    try:
        marcha_db = db.query(DBMarcha).filter(DBMarcha.id == id).first()
        if not marcha_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Marcha no encontrada")
        db.delete(marcha_db)
        db.commit()
        return {"message": "Marcha eliminada correctamente"}
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@marchas_router.post("/migrate/all", status_code=status.HTTP_200_OK)
async def migrate_marchas(db: db_dependency, current_user:current_user):
    try:
        db.query(DBMarcha).delete()
        db.commit()

        marchas = extract_data_marcha("https://glissandoo.com/blog/posts/las-marchas-de-procesion-mas-famosas-de-youtube")
        for marcha in marchas:
            marcha_db = DBMarcha(id=str(uuid.uuid4()), name=marcha["name"], author=marcha["autor"], description=marcha["description"], url=marcha["url"])
            db.add(marcha_db)
        db.commit()
        return {"message": "Migracion realizada correctamente"}
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")