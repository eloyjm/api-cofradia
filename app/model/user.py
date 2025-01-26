from sqlalchemy import ForeignKey, Column, String, Boolean
from sqlalchemy.orm import relationship
from database.postgresdb_manager import db_manager


class User(db_manager.base_schemas):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True)
    username = Column(String(36), unique=True)
    name = Column(String(36))
    surname = Column(String(36))
    email = Column(String(36), nullable=True)
    disabled = Column(Boolean)
    hashed_password = relationship(
        "UserInDB", back_populates="user", cascade="all,delete"
    )


class UserInDB(db_manager.base_schemas):
    __tablename__ = "hashed_passwords"
    hashed_password = Column(String(80))

    username = Column(
        String(36), ForeignKey('users.username'), primary_key=True
    )
    user = relationship("User", back_populates="hashed_password")


class Token(db_manager.base_schemas):
    __tablename__ = "tokens"
    access_token = Column(String(255), primary_key=True)
    token_type = Column(String(50))


class TokenData(db_manager.base_schemas):
    __tablename__ = "tokens_data"
    username = Column(String(36), nullable=True, primary_key=True)


class UsedPassResetToken(db_manager.base_schemas):
    __tablename__ = "used_pass_reset_tokens"
    token = Column(String(255), primary_key=True)
