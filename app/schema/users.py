from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    name: str
    surname: str
    email: Union[str, None] = None
    disabled: bool


class UserInDB(User):
    hashed_password: str


class NewPassword(BaseModel):
    new_pass: str
    confirmation_pass: str


class UserRegister(BaseModel):
    username: str
    name: str
    surname: str
    email: Union[str, None] = None
    password: str


class UserRegisterCMS(BaseModel):
    username: str
    name: str
    surname: str
    email: Union[str, None] = None
    password: str


class UserRegisterAdmin(BaseModel):
    username: str
    name: str
    surname: str
    email: Union[str, None] = None


class UserUpdate(BaseModel):
    name: Union[str, None] = None
    surname: Union[str, None] = None
    email: Union[str, None] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
