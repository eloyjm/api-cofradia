from repository.hermandad_repository import HermandadRepository
from model.hermandades import DayEnum
from fastapi import HTTPException, UploadFile, File
from config.logging.logger import logger
from schema.hermandades import UpdateHermandad
import os
import tensorflow_hub as hub
import numpy as np
import tensorflow as tf
from PIL import Image
from io import BytesIO
import cv2


class HermandadService:

    def __init__(self, hermandad_repository: HermandadRepository):
        self.hermandad_repository = hermandad_repository

    def get_hermandades(self):
        return self.hermandad_repository.get_all_hermanades()

    def get_hermandad_by_day(self, day: DayEnum):
        return self.hermandad_repository.get_hermandad_by_day(day)

    def get_hermandad_by_id(self, id: int):
        hermandad = self.hermandad_repository.get_hermandad_by_id(id)
        if not hermandad:
            message = f"Hermandad with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

    def update_hermandad(self, id: int, hermandad_body: UpdateHermandad):
        hermandad = self.hermandad_repository.update_hermandad(
            id, hermandad_body
        )
        if not hermandad:
            message = f"Hermandad with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return hermandad

    async def run_prediction(self, day: DayEnum, img: UploadFile = File(...)):
        try:
            hermandades = self.get_hermandad_by_day(day)
            if not hermandades:
                message = f"No hermandades found for day {day}"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)
            hermandades = sorted(hermandades, key=lambda x: x.name)

            if day == DayEnum.DDR:
                return [(hermandades[0], 1.0)]

            predictions = await self.categorize_image(img, day)
            logger.info(f"Predictions: {predictions}")
            if not predictions:
                message = "No predictions found"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)

            return [
                (hermandad, round(float(prob), 2))
                for (prediction, prob) in predictions
                for i, hermandad in enumerate(hermandades)
                if i == prediction
            ]
        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

    async def run_full_prediction(self, img: UploadFile = File(...)):
        try:
            hermandades = self.hermandad_repository.get_all_hermanades()
            if not hermandades:
                message = "No hermandades found"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)
            hermandades = sorted(hermandades, key=lambda x: x.name)

            predictions = await self.categorize_image(img, full_model=True)
            logger.info(f"Predictions: {predictions}")
            if not predictions:
                message = "No predictions found"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)

            return [
                (hermandad, round(float(prob), 2))
                for (prediction, prob) in predictions
                for i, hermandad in enumerate(hermandades)
                if i == prediction
            ]

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))

    async def categorize_image(self, img, day=None, full_model=False):
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)
            )))

            if full_model:
                model_path = os.path.join(
                    current_dir,
                    'ia',
                    'models',
                    'FULLDENSENET100.h5'
                )
            else:
                if not day:
                    message = "Day must be provided"
                    logger.error(message)
                    raise HTTPException(status_code=400, detail=message)

                model_path = os.path.join(
                    current_dir,
                    'ia',
                    'models',
                    day._name_,
                    f"{day._name_}DENSENET100.h5"
                )

            model = tf.keras.models.load_model(
                model_path, custom_objects={'KerasLayer': hub.KerasLayer}
            )
            if not model:
                message = "Model not found"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)

            img = Image.open(BytesIO(img.file.read()))
            img = np.array(img).astype(float) / 255
            img = cv2.resize(img, (224, 224))

            if img.shape == (224, 224, 4):
                img = img[:, :, 0:3]

            prediction = model.predict(img.reshape(-1, 224, 224, 3))
            logger.info(f"Prediction: {prediction}")

            top_n = 10 if full_model else 5
            index = np.argsort(prediction[0])[-top_n:][::-1]
            probs = prediction[0][index]
            res = list(zip(index, probs))
            return res

        except Exception as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=str(e))
