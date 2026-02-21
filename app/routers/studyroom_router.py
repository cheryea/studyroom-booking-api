# app/routers/studyroom_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

from app.schemas.studyroom import StudyRoomResponse
from app.services.studyroom_service import studyroom_service


router = APIRouter(prefix="/studyroom", tags=["studyroom"])

@router.get("", response_model=list[StudyRoomResponse])
def read_studyrooms(floor: int = None, min_capacity: int = None, db: Session = Depends(get_db)):
    return studyroom_service.read_studyrooms(
    db,
    floor=floor,
    min_capacity=min_capacity
)

