from database.postgresdb_manager import DatabaseManager
from schema.users import UserSchema
from models.users import User, HashUser
import uuid
from typing import List, Optional
from sqlalchemy.orm import joinedload


class UserRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = next(db_manager.get_db())

    def create_user(self, user_schema: UserSchema, hash_password: str) -> User:
        user = User(**user_schema.model_dump(exclude={"password"}))
        user.id = str(uuid.uuid4())
        self.db.add(user)

        hash_user = HashUser(
            username=user_schema.username, hashed_password=hash_password
        )
        self.db.add(hash_user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def get_users(self) -> List[User]:
        return self.db.query(User).all()

    def get_hash_user(self, username: str) -> Optional[HashUser]:
        return (
            self.db.query(HashUser)
            .filter(HashUser.username == username)
            .options(joinedload(HashUser.user))
            .first()
        )
