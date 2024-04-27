from pydantic import BaseModel
from typing import Optional

class UpdateHermandad(BaseModel):
    description: Optional[str]
    foundation: Optional[str]
    members: Optional[str]
    nazarenos: Optional[str]
    history: Optional[str]
    passages_number: Optional[str]
    location: Optional[str]
    colors: Optional[str]
    color_one: Optional[str]
    color_two: Optional[str]
    day_time: Optional[str]
    canonical_seat: Optional[str]
    wiki_url: Optional[str]
    route_url: Optional[str]
