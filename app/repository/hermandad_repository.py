from database.postgresdb_manager import DatabaseManager
from models.hermandades import Hermandad, DayEnum
from sqlalchemy.orm import joinedload
from schema.hermandades import UpdateHermandad
from config.logging.logger import logger
from typing import List, Optional


class HermandadRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

    def commit(self):
        self.db.commit()

    def get_all_hermanades(self) -> List[Hermandad]:
        return self.db.query(Hermandad).all()

    def get_hermandad_by_day(self, day: DayEnum) -> List[Hermandad]:
        return (
            self.db.query(Hermandad)
            .filter(Hermandad.day == day)
            .options(joinedload(Hermandad.timetables))
            .all()
        )

    def get_hermandad_by_id(self, id: int) -> Optional[Hermandad]:
        return self.db.query(Hermandad).filter(Hermandad.id == id).first()

    def update_hermandad(
        self, id, hermandad_body: UpdateHermandad
    ) -> Optional[Hermandad]:
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

    def update_hermandad_from_wiki(self, hermandad: Hermandad, data: dict):
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

    def create_all_hermandades(
        self, hermandades: List[Hermandad]
    ) -> List[Hermandad]:
        for hermandad in hermandades:
            self.db.add(hermandad)
        self.db.commit()

        return "All hermandades migrated"

    def delete_all_hermandades(self) -> str:
        self.db.query(Hermandad).delete()
        self.db.commit()
        return "Successfully deleted all hermandades"
