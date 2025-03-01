from PIL import Image
from io import BytesIO
import cv2
import os
import numpy as np
from config.logging.logger import logger
from fastapi import HTTPException
from typing import List

import tensorflow_hub as hub

import tensorflow as tf


async def categorize_image(img, full_model, day=None) -> List:
    try:
        current_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        if full_model:
            model_path = os.path.join(
                current_dir, "app", "ai", "models", "FULLDENSENET100.h5"
            )
        else:
            if not day:
                message = "Day must be provided"
                logger.error(message)
                raise HTTPException(status_code=400, detail=message)

            model_path = os.path.join(
                current_dir,
                "app",
                "ai",
                "models",
                day._name_,
                f"{day._name_}DENSENET100.h5",
            )

        models = tf.keras.models.load_model(
            model_path, custom_objects={"KerasLayer": hub.KerasLayer}
        )
        if not models:
            message = "Model not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        img = Image.open(BytesIO(img.file.read()))
        img = np.array(img).astype(float) / 255
        img = cv2.resize(img, (224, 224))

        if img.shape == (224, 224, 4):
            img = img[:, :, 0:3]

        prediction = models.predict(img.reshape(-1, 224, 224, 3))
        logger.info(f"Prediction: {prediction}")

        top_n = 10 if full_model else 5
        index = np.argsort(prediction[0])[-top_n:][::-1]
        probs = prediction[0][index]
        res = list(zip(index, probs))
        return res

    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))
