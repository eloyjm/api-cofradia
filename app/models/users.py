from sqlalchemy import ForeignKey, Column, String, Boolean
from sqlalchemy.orm import relationship
from database.postgresdb_manager import db_manager


class User(db_manager.base_schemas):
    __tablename__ = "user"
    id = Column(String(36), primary_key=True)
    username = Column(String(36), unique=True)
    name = Column(String(36))
    surname = Column(String(36))
    email = Column(String(36), nullable=True)
    disabled = Column(Boolean)
    hash_user = relationship(
        "HashUser", back_populates="user", cascade="all,delete"
    )


class HashUser(db_manager.base_schemas):
    __tablename__ = "hash_user"
    hashed_password = Column(String(80))

    username = Column(
        String(36), ForeignKey("user.username"), primary_key=True
    )
    user = relationship("User", back_populates="hash_user")


# class Token(db_manager.base_schemas):
#     __tablename__ = "token"
#     access_token = Column(String(255), primary_key=True)
#     token_type = Column(String(50))


# class TokenData(db_manager.base_schemas):
#     __tablename__ = "tokens_data"
#     username = Column(String(36), nullable=True, primary_key=True)


# class UsedPassResetToken(db_manager.base_schemas):
#     __tablename__ = "used_pass_reset_tokens"
#     token = Column(String(255), primary_key=True)
