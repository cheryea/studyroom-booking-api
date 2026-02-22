# app/schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enum import Enum
from app.schemas.studyroom import StudyRoomSimpleResponse


# Reservation
class ReservationStatus(str, Enum):
    RESERVED = "RESERVED"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

class ReservationCreate(BaseModel):
    studyroom_id: int
    start_datetime: datetime
    end_datetime: datetime

class ReservationResponse(BaseModel):
    id: int
    user_id: int
    studyroom: StudyRoomSimpleResponse
    start_datetime: datetime
    end_datetime: datetime
    status: ReservationStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)