# app/schemas.py
from pydantic import BaseModel, ConfigDict

# StudyRoom
class StudyRoomResponse(BaseModel):
    id: int
    name: str
    floor: int
    location: str
    capacity: int
    facilities: list[str] = []

    model_config = ConfigDict(from_attributes=True)
