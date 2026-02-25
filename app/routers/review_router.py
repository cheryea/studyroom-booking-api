# app/routers/review_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from dependencies import get_current_user
from app.models import User, Reservation, ReservationStatus
from app.services.review_service import review_service
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["reviews"])


# ----- 예약 단위 내 리뷰 CRUD (1:1, 본인만) -----

@router.post(
    "/reservation/{reservation_id}",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_review(
    reservation_id: int,
    data: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    예약에 대한 리뷰 작성.
    동작: 예약 조회 → 본인 예약·COMPLETED·중복 여부 검증 후 생성.
    """
    return review_service.create(db, reservation_id, data, current_user)

@router.get(
    "/reservation/{reservation_id}",
    response_model=ReviewResponse,
)
def get_review(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    예약 단위 내 리뷰 조회.
    동작: 예약 소유권 확인 후 해당 예약의 리뷰 반환, 없으면 404.
    """
    return review_service.get_by_reservation(db, reservation_id, current_user)


@router.put(
    "/reservation/{reservation_id}",
    response_model=ReviewResponse,
)
def update_review(
    reservation_id: int,
    data: ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    예약에 대한 리뷰 수정.
    동작: 리뷰 존재·본인 소유 확인 후 수정.
    """
    return review_service.update(db, reservation_id, data, current_user)


@router.delete(
    "/reservation/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_review(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    예약에 대한 리뷰 삭제.
    동작: 리뷰 존재·본인 소유 확인 후 삭제.
    """
    review_service.delete(db, reservation_id, current_user)


# ----- 스터디룸 전체 리뷰 조회 (1:N, 페이지네이션·정렬) -----

@router.get(
    "/studyroom/{room_id}",
    response_model=list[ReviewResponse],
)
def get_studyroom_reviews(
    room_id: int,
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    sort: str | None = "recent",
):
    """
    스터디룸별 전체 리뷰 목록.
    동작: 스터디룸 존재 확인 후 limit/offset, sort=recent 적용하여 반환.
    """
    return review_service.get_by_studyroom(
        db, room_id, limit=limit, offset=offset, sort=sort
    )

# ----- 예약 완료 처리 (개발자용) -----
@router.patch("/reservations/{reservation_id}/complete")
def complete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    if reservation.status == ReservationStatus.COMPLETED:
        return {"detail": "이미 완료된 예약입니다."}

    reservation.status = ReservationStatus.COMPLETED
    db.commit()
    db.refresh(reservation)  # DB 커밋 후 최신 상태 반영
    return reservation