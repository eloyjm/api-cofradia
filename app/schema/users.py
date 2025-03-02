from pydantic import BaseModel
from typing import Union


class UserSchema(BaseModel):
    username: str
    name: str
    surname: str
    email: Union[str, None] = None
    disabled: bool
    password: str
