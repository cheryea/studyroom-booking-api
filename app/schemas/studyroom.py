# app/schemas.py
from pydantic import BaseModel, ConfigDict
from app.schemas.facility import FacilityResponse

# StudyRoom
class StudyRoomResponse(BaseModel):
    id: int
    name: str
    floor: int
    location: str
    capacity: int
    facilities: list[FacilityResponse] = []

    model_config = ConfigDict(from_attributes=True)

class StudyRoomSimpleResponse(BaseModel):
    name: str
    floor: int

    model_config = ConfigDict(from_attributes=True)
