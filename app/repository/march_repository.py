from typing import List, Optional
from database.postgresdb_manager import DatabaseManager
from models.marchs import March
from schema.marchs import MarchSchema


class MarchRepository:

    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

    def get_all_marchs(self) -> List[March]:
        return self.db.query(March).all()

    def get_march_by_id(self, id: int) -> Optional[March]:
        return self.db.query(March).filter(March.id == id).first()

    def create_march(self, march_data: MarchSchema) -> March:
        new_march = March(**march_data.model_dump())
        self.db.add(new_march)
        self.db.commit()
        self.db.refresh(new_march)
        return new_march

    def delete_march(self, id: int) -> Optional[str]:
        march = self.get_march_by_id(id)
        if march:
            self.db.delete(march)
            self.db.commit()
            return "Successfully deleted"
        return None

    def delete_all(self) -> str:
        self.db.query(March).delete()
        self.db.commit()
        return "Successfully deleted all marches"
