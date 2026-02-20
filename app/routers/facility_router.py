# routers/facility_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.facility import FacilityResponse
from app.services.facility_service import facility_service

router = APIRouter(prefix="/facilities", tags=["facilities"])


@router.get("", response_model=list[FacilityResponse])
def read_facilities(db: Session = Depends(get_db)):
    return facility_service.read_facilities(db)
