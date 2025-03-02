from repository.user_repository import UserRepository
from schema.users import UserSchema
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from config.logging.logger import logger
from util import user_util
from models.users import User, HashUser
from typing import List, Optional
from passlib.context import CryptContext


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def sign_up(self, user_schema: UserSchema) -> User:
        registered = self.user_repository.get_hash_user(user_schema.username)
        if registered:
            message = f"Username {user_schema.username} already used."
            logger.error(message)
            raise HTTPException(status_code=400, detail=message)

        hash_password = user_util.password_validator(user_schema.password)

        user = self.user_repository.create_user(user_schema, hash_password)

        return user

    def sign_in(self, form_data: OAuth2PasswordRequestForm):
        user = self.authenticate_user(form_data.username, form_data.password)
        if not user:
            message = "Invalid credentials."
            logger.error(message)
            raise HTTPException(
                status_code=401,
                detail=message,
                headers={"WWW-Authenticate": "Bearer"},
            )

        return {
            "access_token": user_util.create_access_token(user.username),
            "token_type": "bearer",
        }

    def authenticate_user(
        self, username: str, password: str
    ) -> Optional[HashUser]:
        user = self.user_repository.get_hash_user(username)
        if not user or not self.pwd_context.verify(
            password, user.hashed_password
        ):
            return None
        return user

    def get_users(self) -> List[User]:
        return self.user_repository.get_users()
