# app/schemas.py
from pydantic import BaseModel

# StudyRoom
class StudyRoomResponse(BaseModel):
    id: int
    name: str
    floor: int
    capacity: int
    location: str

    # class Config:
    #     orm_mode = True
