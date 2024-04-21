from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from ..db.models.hermandades import Hermandad as DBHermandad
from ..db.models.hermandades import DayEnum
from sqlalchemy.orm import Session, joinedload
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from ..db.database import get_db
from ..schemas.hermandades import UpdateHermandad
from PIL import Image
from io import BytesIO
import cv2
from starlette.responses import FileResponse
import shutil
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import os
from ..db.migrations.scraping import extract_data_wiki
from ..routers.oauth import  get_current_user
from ..schemas import users

hermandades_router = APIRouter(tags=["hermandades"])
db_dependency = Annotated[Session, Depends(get_db)]
current_user = Annotated[users.User, Depends(get_current_user)]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESCUDO_DIR = os.path.join(BASE_DIR, "static/images/escudos/")
TRAJE_DIR = os.path.join(BASE_DIR, "static/images/trajes/")

@hermandades_router.get('/hermandades', status_code=status.HTTP_200_OK)
async def get_hermandades(db: db_dependency):
    try:
        hermandades = db.query(DBHermandad).all()
        return hermandades
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")


@hermandades_router.get('/hermandades/day/{day}', status_code=status.HTTP_200_OK)
async def get_hermandades_by_day(db: db_dependency, day: DayEnum):
    try:
        hermandades = db.query(DBHermandad).filter(DBHermandad.day == day).options(joinedload(DBHermandad.timetables)).all()
        return hermandades
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.get('/hermandades/{id}', status_code=status.HTTP_200_OK)
async def get_hermandades_by_id(db: db_dependency, id: str):
    try:
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        return hermandad
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@hermandades_router.patch('/hermandades/update/{id}', status_code=status.HTTP_200_OK)
async def update_hermandad(db: db_dependency, id: str, hermandad_data: UpdateHermandad, current_user: current_user):
    try:
        hermandad_db = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if not hermandad_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la hermandad con id:{id}")
        print(hermandad_data)
        for key, value in hermandad_data.model_dump(exclude_unset=True).items():
            setattr(hermandad_db, key, value)

        db.commit()
        db.refresh(hermandad_db)
        return hermandad_db
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@hermandades_router.post('/prediction', status_code=status.HTTP_200_OK)
def get_hermandad_prediction(db: db_dependency, day: DayEnum , img : UploadFile = File(...)):
    try:

        her_data=get_hermandades_by_day(db, day)
        if len(her_data)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado ninguna hermandad")
        her_data = sorted(her_data, key=lambda x: x.name)
        
        if day == DayEnum.DDR:
            return [(her_data[0], 1.0)]
        
        predicciones = categorizar(img, day)
        print("Predicciones:", predicciones)
        if len(predicciones)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha podido predecir")

        return [(hermandad, round(float(prob),2)) for (prediccion,prob) in predicciones for i, hermandad in enumerate(her_data) if i == prediccion]

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

def categorizar(img: UploadFile, day: DayEnum):
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(current_dir, 'ia', 'models', day._name_, day._name_+'DENSENET100.h5')
    print(model_path)
    model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado el modelo")
    
    img = Image.open(BytesIO(img.file.read()))
    img = np.array(img).astype(float)/255
    img = cv2.resize(img, (224,224))

    if img.shape == (224, 224, 4):
        img = img[:,:,0:3]

    prediccion = model.predict(img.reshape(-1, 224, 224, 3))
    print(prediccion)
    indices = np.argsort(prediccion[0])[-5:][::-1]
    probabilidades = prediccion[0][indices]
    res = list(zip(indices, probabilidades))
    return res

@hermandades_router.post('/prediction/full', status_code=status.HTTP_200_OK)
def get_hermandad_prediction(db: db_dependency, img : UploadFile = File(...)):
    try:
        her_data=get_hermandades(db)
        if len(her_data)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado ninguna hermandad")
        her_data = sorted(her_data, key=lambda x: x.name)

        predicciones = categorizar_full(img)
        print("Predicciones:", predicciones)
        if len(predicciones)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha podido predecir")

        return [(hermandad, round(float(prob),2)) for (prediccion,prob) in predicciones for i, hermandad in enumerate(her_data) if i == prediccion]
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

def categorizar_full(img: UploadFile):
    current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    model_path = os.path.join(current_dir, 'ia', 'models','FULLDENSENET100.h5')
    print(model_path)
    model = tf.keras.models.load_model(model_path, custom_objects={'KerasLayer': hub.KerasLayer})
    if not model:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado el modelo")
    
    img = Image.open(BytesIO(img.file.read()))
    img = np.array(img).astype(float)/255
    img = cv2.resize(img, (224,224))

    if img.shape == (224, 224, 4):
        img = img[:,:,0:3]

    prediccion = model.predict(img.reshape(-1, 224, 224, 3))
    print(prediccion)
    indices = np.argsort(prediccion[0])[-10:][::-1]
    probabilidades = prediccion[0][indices]
    res = list(zip(indices, probabilidades))
    return res

@hermandades_router.patch('/migrate/wiki', status_code=status.HTTP_200_OK)
async def parse_wiki(db: db_dependency, current_user: current_user):
    try:
        hermandades = db.query(DBHermandad).all()
        for hermandad in hermandades:
            if hermandad.wiki_url:
                data = extract_data_wiki(hermandad.wiki_url)
                hermandad.description = data["Descripcción"]
                hermandad.foundation = data["Fundación"]
                hermandad.members = data["Hermanos"].replace("[cita requerida]", "")
                hermandad.nazarenos = data["Nazarenos"]
                hermandad.history = data["Historia"]
                hermandad.passages_number = data["Pasos"]
                hermandad.location = data["Localidad"]
                hermandad.colors = data["Túnica"]
                hermandad.day_time = data["Día y hora"]
                hermandad.canonical_seat = data["Sede canónica"]

                db.add(hermandad)
            db.commit()
        return {"message": "Datos actualizados"}
        

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@hermandades_router.patch('/migrate/wiki/day/{day}', status_code=status.HTTP_200_OK)
async def parse_wiki_day(db: db_dependency, day: DayEnum, current_user: current_user):
    try:
        hermandades = db.query(DBHermandad).filter(DBHermandad.day == day).all()
        for hermandad in hermandades:
            if hermandad.wiki_url:
                data = extract_data_wiki(hermandad.wiki_url)
                hermandad.description = data["Descripcción"]
                hermandad.foundation = data["Fundación"]
                hermandad.members = data["Hermanos"].replace("[cita requerida]", "")
                hermandad.nazarenos = data["Nazarenos"]
                hermandad.history = data["Historia"]
                hermandad.passages_number = data["Pasos"]
                hermandad.location = data["Localidad"]
                hermandad.colors = data["Túnica"]
                hermandad.day_time = data["Día y hora"]
                hermandad.canonical_seat = data["Sede canónica"]

                db.add(hermandad)
            db.commit()
        return {"message": "Datos actualizados"}
        

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@hermandades_router.patch('/migrate/wiki/{id}', status_code=status.HTTP_200_OK)
async def parse_wiki_by_id(db: db_dependency, id:str, current_user:current_user):
    try:
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if hermandad.wiki_url:
            data = extract_data_wiki(hermandad.wiki_url)
            hermandad.description = data["Descripcción"]
            hermandad.foundation = data["Fundación"]
            hermandad.members = data["Hermanos"].replace("[cita requerida]", "")
            hermandad.nazarenos = data["Nazarenos"]
            hermandad.history = data["Historia"]
            hermandad.passages_number = data["Pasos"]
            hermandad.location = data["Localidad"]
            hermandad.colors = data["Túnica"]
            hermandad.day_time = data["Día y hora"]
            hermandad.canonical_seat = data["Sede canónica"]

            db.add(hermandad)
        db.commit()
        return {"message": "Datos actualizados"}
        

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.put('/hermandades/update/{id}/image/escudo', status_code=status.HTTP_200_OK)
async def update_hermandad_image_escudo(db: db_dependency, current_user: current_user, id: str, img : UploadFile = File(...) ):
    try:
        hermandad_db = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if not hermandad_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la hermandad con id:{id}")
        
        os.makedirs(ESCUDO_DIR, exist_ok=True)
        file_location = os.path.join(ESCUDO_DIR, img.filename)

        with open(file_location, "wb") as image:
            shutil.copyfileobj(img.file, image)
      
        hermandad_db.escudo_url = img.filename
        db.commit()
        db.refresh(hermandad_db)

        return hermandad_db
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.put('/hermandades/update/{id}/image/traje', status_code=status.HTTP_200_OK)
async def update_hermandad_image_traje(db: db_dependency, current_user: current_user, id: str, img : UploadFile = File(...) ):
    try:
        hermandad_db = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if not hermandad_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la hermandad con id:{id}")
        
        os.makedirs(TRAJE_DIR, exist_ok=True)
        file_location = os.path.join(TRAJE_DIR, img.filename)

        with open(file_location, "wb") as image:
            shutil.copyfileobj(img.file, image)
      
        hermandad_db.traje_url = img.filename
        db.commit()
        db.refresh(hermandad_db)

        return hermandad_db
    
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.get('/hermandades/{id}/image/escudo', status_code=status.HTTP_200_OK)
async def get_hermandad_image_escudo(db: db_dependency, current_user: current_user, id: str):
    try:
        hermandad_db = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if not hermandad_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la hermandad con id:{id}")
        
        file_location = os.path.join(ESCUDO_DIR, hermandad_db.escudo_url)

        if not os.path.exists(file_location):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la imagen del escudo")
        
        return FileResponse(file_location, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.get('/hermandades/{id}/image/traje', status_code=status.HTTP_200_OK)
async def get_hermandad_image_traje(db: db_dependency, current_user: current_user, id: str):
    try:
        hermandad_db = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        if not hermandad_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la hermandad con id:{id}")
        
        file_location = os.path.join(TRAJE_DIR, hermandad_db.traje_url)

        if not os.path.exists(file_location):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado la imagen del traje")
        
        return FileResponse(file_location, headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
    except HTTPException as h:
        raise h
    except Exception as e:
        print("error:", e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")