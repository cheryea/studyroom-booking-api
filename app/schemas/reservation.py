# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


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
    studyroom_id: int
    start_datetime: datetime
    end_datetime: datetime
    status: ReservationStatus
    created_at: datetime

    # class Config:
    #     orm_mode = True