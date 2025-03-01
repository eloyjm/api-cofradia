from typing import List
from models.marchs import March
from config.logging.logger import logger
from fastapi import HTTPException
from util import scrapping_util
from config.app import config_app
from schema.marchs import MarchSchema
from repository.march_repository import MarchRepository


class MarchService:

    def __init__(self, march_repository: MarchRepository):
        self.march_repository = march_repository

    def get_marchs(self) -> List[March]:
        return self.march_repository.get_all_marchs()

    def get_march_by_id(self, id: int) -> March:
        march = self.march_repository.get_march_by_id(id)
        if not march:
            message = f"March with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return march

    def create_march(self, march: MarchSchema) -> March:
        return self.march_repository.create_march(march)

    def delete_march(self, id: int) -> str:
        march = self.march_repository.delete_march(id)
        if not march:
            message = f"March with id {id} not found"
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        return march

    def migrate_all(self) -> str:
        self.march_repository.delete_all()

        marchs = scrapping_util.extract_data_marcha(config_app.marchs_url)
        for march in marchs:
            self.march_repository.create_march(MarchSchema(**march))
            logger.info(f"March {march['name']} migrated")

        return "Migrated all marchs"
