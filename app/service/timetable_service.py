from models.timetables import Timetable
from repository.timetable_repository import TimetableRepository
from typing import List
from config.logging.logger import logger
from fastapi import HTTPException
from schema.timetables import TimetableSchema
from service.hermandad_service import HermandadService
from unidecode import unidecode
from config.mappings import name_mapping
from util import scrapping_util
from config.app import config_app
from models.hermandades import Hermandad


class TimetableService:

    def __init__(
        self,
        timetable_repository: TimetableRepository,
        hermandad_service: HermandadService,
    ):
        self.timetable_repository = timetable_repository
        self.hermandad_service = hermandad_service

    def get_timetables(self) -> List[Timetable]:
        return self.timetable_repository.get_all_timetables()

    def get_timetables_by_id(self, id: int) -> Timetable:
        timetable = self.timetable_repository.get_timetable_by_id(id)
        if not timetable:
            message = f"Timetable with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return timetable

    def get_timetables_by_hermandad(self, her_id: int) -> List[Timetable]:
        timetables = self.timetable_repository.get_timetables_by_hermandad(
            her_id
        )
        if not timetables:
            message = f"No timetables found for hermandad {her_id}"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return timetables

    def create_timetable(self, timetable_schema: TimetableSchema) -> Timetable:
        timetable = self.timetable_repository.create_timetable(
            timetable_schema
        )
        if not timetable:
            message = (
                f"Hermandad with id {timetable_schema.hermandad_id} not found"
            )
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)
        self.timetable_repository.commit()

        return timetable

    def delete_timetable(self, id: int) -> str:
        timetable = self.timetable_repository.delete_timetable(id)
        if not timetable:
            message = f"Timetable with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return timetable

    def migrate_all_timetables(self) -> str:
        self.timetable_repository.delete_all_timetables()

        hermandades = self.hermandad_service.get_hermandades()
        for hermandad in hermandades:
            self.process_timetable(hermandad)

        self.timetable_repository.commit()

        return "Timetables migrated successfully"

    def process_timetable(self, hermandad: Hermandad):
        try:
            name = unidecode(hermandad.name.lower().replace(" ", "-"))

            name = name_mapping.get(name, name)
            url = config_app.dds_url + "/" + name + ".php"

            data, map_src = scrapping_util.extract_data_dds(url)

            if map_src:
                hermandad.route_url = map_src
            for row in data:
                row["hermandad_id"] = hermandad.id
                self.timetable_repository.create_timetable(
                    TimetableSchema(**row)
                )

            logger.info(f"Timetable created for {hermandad.name}")

        except Exception as e:
            message = f"Error processing timetable for {hermandad.name} - {e}"
            logger.error(message)
            raise HTTPException(
                status_code=500,
                detail=message,
            )
