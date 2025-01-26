from database.postgresdb_manager import DatabaseManager
from model.hermandades import Hermandad, DayEnum
from sqlalchemy.orm import joinedload
from schema.hermandades import UpdateHermandad
from config.logging.logger import logger


class HermandadRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

    def get_all_hermanades(self):
        return self.db.query(Hermandad).all()

    def get_hermandad_by_day(self, day: DayEnum):
        return self.db.query(Hermandad).filter(Hermandad.day == day).options(
            joinedload(Hermandad.timetables)
        ).all()

    def get_hermandad_by_id(self, id: int):
        return self.db.query(Hermandad).filter(Hermandad.id == id).first()

    def update_hermandad(self, id,  hermandad_body: UpdateHermandad):
        hermandad = self.get_hermandad_by_id(id)
        if hermandad:
            for key, value in hermandad_body.model_dump(
                exclude_unset=True
            ).items():
                setattr(hermandad, key, value)
            self.db.commit()
            self.db.refresh(hermandad)
            logger.info(f"Hermandad {hermandad.name} updated")
            return hermandad
        return None
