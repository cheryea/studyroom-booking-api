# mysite4/routers/reservation_router.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.services.reservation_service import reservation_service
from app.schemas.reservation import ReservationCreate, ReservationResponse
from dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/reservations", tags=["reservations"])


@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
def create_reservation(
    data: ReservationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),  # 로그인한 유저 자동 주입
):
    return reservation_service.create_reservation(db, data, current_user)


@router.get(
    "/mine",
    response_model=list[ReservationResponse]
)
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return reservation_service.get_my_reservations(db, current_user)

