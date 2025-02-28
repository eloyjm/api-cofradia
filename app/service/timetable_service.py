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
import re
from datetime import datetime


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
        return self.timetable_repository.create_timetable(timetable_schema)

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
        map(self.process_timetable, hermandades)

        return "Timetables migrated successfully"

    def migrate_day_timetables(self, day: str) -> str:
        self.timetable_repository.delete_all_timetables()

        hermandades = self.hermandad_service.get_hermandades_by_day(day)
        map(self.process_timetable, hermandades)

        return "Timetables migrated successfully"

    def migrate_hermandad_timetables(self, her_id: int) -> str:
        self.timetable_repository.delete_timetables_by_hermandad(her_id)

        hermandad = self.hermandad_service.get_hermandad_by_id(her_id)
        self.process_timetable(hermandad)

        return "Timetables migrated successfully"

    def process_timetable(self, hermandad: Hermandad):
        try:
            name = unidecode(hermandad.name.lower().replace(" ", "-"))

            name = name_mapping.get(name, name)
            url = config_app.dds_url + name + ".php"
            data, map_src = scrapping_util.extract_data_dds(url)
            if map_src:
                hermandad.route_url = map_src
            for row in data:
                time = row[1]
                location = row[2]
                match = re.search(r"\((.*?)\)", location)
                if match:
                    time = match.group(1)
                    location = re.sub(r"\(.*?\)", "", location)

                if time != "":
                    time = datetime.strptime(
                        time.replace(".", ":"), "%H:%M"
                    ).time()
                    if not time:
                        message = f"Incorrect time format {time}"
                        logger.error(message)
                        raise HTTPException(
                            status_code=400,
                            detail=message,
                        )
                    self.create_timetable(
                        TimetableSchema(
                            time=time,
                            entity=row[0],
                            location=location,
                            hermandad=hermandad,
                        )
                    )
                    logger.info(f"Timetable created for {hermandad.name}")

        except Exception as e:
            message = f"Error processing timetable for {hermandad.name} - {e}"
            logger.error(message)
            raise HTTPException(
                status_code=500,
                detail=message,
            )
