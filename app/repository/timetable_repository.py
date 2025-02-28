from database.postgresdb_manager import DatabaseManager
from models.timetables import Timetable
from typing import List, Optional
from schema.timetables import TimetableSchema


class TimetableRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

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

    def create_timetable(self, timetable_schema: TimetableSchema) -> Timetable:
        new_Timetable = Timetable(**timetable_schema.model_dump())
        self.db.add(new_Timetable)
        self.db.commit()
        self.db.refresh(new_Timetable)
        return new_Timetable

    def delete_timetable(self, id: int) -> Optional[str]:
        timetable = self.get_timetable_by_id(id)
        if timetable:
            self.db.delete(timetable)
            self.db.commit()
            return "Successfully deleted"
        return None
