from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from app.db.models.hermandades import Hermandad as DBHermandad
from app.db.models.hermandades import DayEnum
from sqlalchemy.orm import Session
from typing import Annotated
from app.db.database import get_db
from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
import os


hermandades_router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]


@hermandades_router.get('/hermandades', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandades(db: db_dependency):
    try:
        hermandades = db.query(DBHermandad).all()
        return hermandades
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")


@hermandades_router.get('/hermandades/{day}', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandades_by_day(db: db_dependency, day: DayEnum):
    try:
        hermandades = db.query(DBHermandad).filter(DBHermandad.day == day).all()
        return hermandades
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.get('/hermandades/{id}', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandades_by_id(db: db_dependency, id: int):
    try:
        hermandad = db.query(DBHermandad).filter(DBHermandad.id == id).first()
        return hermandad
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
    
@hermandades_router.post('/prediction', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandad_prediction(db: db_dependency, day: DayEnum , img : UploadFile = File(...)):
    #try:
        print(img)
        print(day)
        predicciones = categorizar(img, day)
        if len(predicciones)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha podido predecir")

        her_data=get_hermandades_by_day(db, day)
        if len(her_data)==0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No se ha encontrado ninguna hermandad")
        
        res = [hermandad for prediccion in predicciones for hermandad in her_data if hermandad.her_id == prediccion]

        return res
    
    #except Exception as e:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")

@hermandades_router.post('/prediction/prueba', tags=["hermandades"], status_code=status.HTTP_200_OK)
def get_hermandad_prediction(db: db_dependency, file : UploadFile):
        return {"filename": file.filename}

def categorizar(img: UploadFile, day: DayEnum):
    #try:
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        model_path = os.path.join(current_dir, 'ia', 'models', day._name_, day._name_+'DENSENET100.h5')

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
        
        if (max(prediccion[0]) >= 0.7):
            top = np.argmax(prediccion[0], axis=-1)
            print(top)
            return [top]
        else:

            index = np.argpartition(prediccion[0], -3)[-3:]
            indices = index[np.argsort(-prediccion[0][index])]
            print(indices)
            return indices
    
    #except Exception as e:
    #    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor:{str(e)}")
