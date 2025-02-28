from database.postgresdb_manager import DatabaseManager
from models.timetables import Timetable
from typing import List, Optional
from schema.timetables import TimetableSchema
from models.hermandades import Hermandad


class TimetableRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

    def commit(self):
        self.db.commit()

    def get_all_timetables(self) -> List[Timetable]:
        return self.db.query(Timetable).all()

    def get_timetable_by_id(self, id: int) -> Optional[Timetable]:
        return self.db.query(Timetable).filter(Timetable.id == id).first()

    def get_timetables_by_hermandad(self, her_id: int) -> Optional[Timetable]:
        return (
            self.db.query(Timetable)
            .filter(Timetable.hermandad_id == her_id)
            .all()
        )

    def create_timetable(
        self, timetable_schema: TimetableSchema
    ) -> Optional[Timetable]:
        hermandad = (
            self.db.query(Hermandad)
            .filter(Hermandad.id == timetable_schema.hermandad_id)
            .first()
        )
        if not hermandad:
            return None

        new_timetable = Timetable(**timetable_schema.model_dump())
        self.db.add(new_timetable)

        return "Created"

    def delete_timetable(self, id: int) -> Optional[str]:
        timetable = self.get_timetable_by_id(id)
        if timetable:
            self.db.delete(timetable)
            self.db.commit()
            return "Successfully deleted"
        return None

    def delete_all_timetables(self) -> str:
        self.db.query(Timetable).delete()
        self.db.commit()
        return "All timetables deleted"
