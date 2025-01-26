from pydantic import BaseModel


class Marcha(BaseModel):
    name: str
    author: str
    description: str
    url: str
