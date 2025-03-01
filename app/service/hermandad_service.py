from repository.hermandad_repository import HermandadRepository
from models.hermandades import DayEnum
from fastapi import HTTPException, UploadFile, File
from config.logging.logger import logger
from schema.hermandades import UpdateHermandad
from typing import List, Tuple
from models.hermandades import Hermandad
from util import hermandad_util
from util import scrapping_util
from starlette.responses import FileResponse
import os
from config.app import config_app


class HermandadService:

    def __init__(
        self,
        hermandad_repository: HermandadRepository,
        hermandades_data: List[dict],
    ):
        self.hermandad_repository = hermandad_repository
        self.hermandades_data = hermandades_data

    def get_hermandades(self) -> List[Hermandad]:
        return self.hermandad_repository.get_all_hermanades()

    def get_hermandad_by_day(self, day: DayEnum) -> List[Hermandad]:
        return self.hermandad_repository.get_hermandad_by_day(day)

    def get_hermandad_by_id(self, id: int) -> Hermandad:
        hermandad = self.hermandad_repository.get_hermandad_by_id(id)
        if not hermandad:
            message = f"Hermandad with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return hermandad

    def update_hermandad(
        self, id: int, hermandad_body: UpdateHermandad
    ) -> Hermandad:
        hermandad = self.hermandad_repository.update_hermandad(
            id, hermandad_body
        )
        if not hermandad:
            message = f"Hermandad with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return hermandad

    def populate_all_hermandades(self):
        self.hermandad_repository.delete_all_hermandades()
        hermandades = [
            Hermandad(**hermandad_data)
            for hermandad_data in self.hermandades_data
        ]

        return self.hermandad_repository.create_all_hermandades(hermandades)

    async def run_prediction(
        self, day: DayEnum = None, img: UploadFile = File(...)
    ) -> List[Tuple[Hermandad, float]]:
        try:
            if day:
                hermandades = self.get_hermandad_by_day(day)
                full_mode = False
            else:
                hermandades = self.get_hermandades()
                full_mode = True

            hermandades = sorted(hermandades, key=lambda x: x.name)

            if day == DayEnum.DDR:
                return [(hermandades[0], 1.0)]

            predictions = await hermandad_util.categorize_image(
                img, full_mode, day
            )
            if not predictions:
                message = "No predictions found"
                logger.error(message)
                raise HTTPException(status_code=404, detail=message)

            logger.info(f"Predictions: {predictions}")

            return [
                (hermandad, round(float(prob), 2))
                for (prediction, prob) in predictions
                for i, hermandad in enumerate(hermandades)
                if i == prediction
            ]

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise HTTPException(status_code=500, detail=str(e))

    def migrate_wiki(self, day: DayEnum, id: int) -> str:
        if day:
            hermandades = self.get_hermandad_by_day(day)
        elif id:
            hermandades = [self.get_hermandad_by_id(id)]
        else:
            hermandades = self.get_hermandades()

        for hermandad in hermandades:
            if hermandad.wiki_url:
                data = scrapping_util.extract_data_wiki(hermandad.wiki_url)

                self.hermandad_repository.update_hermandad_from_wiki(
                    hermandad, data
                )
            else:
                logger.warning(f"Hermandad {hermandad.name} has no wiki url")

        self.hermandad_repository.commit()

        return "Wiki data migrated successfully"

    def get_hermandad_shield(self, id: int) -> bytes:
        hermandad = self.get_hermandad_by_id(id)

        path_location = os.path.normpath(
            os.path.join(config_app.base_path, config_app.shield_path)
        )
        file_location = os.path.join(path_location, hermandad.shield_path)
        if not os.path.exists(file_location):
            message = (
                f"Shield image for hermandad {id} not found: {file_location}"
            )
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return FileResponse(
            file_location,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )

    def get_hermandad_suit(self, id: int) -> bytes:
        hermandad = self.get_hermandad_by_id(id)
        path_location = os.path.normpath(
            os.path.join(config_app.base_path, config_app.suit_path)
        )
        file_location = os.path.join(path_location, hermandad.suit_path)

        if not os.path.exists(file_location):
            message = (
                f"Suit image for hermandad {id} not found: {file_location}"
            )
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return FileResponse(
            file_location,
            headers={"Cache-Control": "no-cache, no-store, must-revalidate"},
        )
