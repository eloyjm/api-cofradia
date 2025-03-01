from pydantic import BaseModel


class MarchSchema(BaseModel):
    name: str
    author: str
    description: str
    url: str
