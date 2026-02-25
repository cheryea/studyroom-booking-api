# app/services/review_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User, ReservationStatus, Review, StudyRoom
from app.repositories.reservation_repository import reservation_repository
from app.repositories.review_repository import review_repository
from app.schemas.review import ReviewCreate, ReviewUpdate


class ReviewService:
    """리뷰 비즈니스 로직: 예약 단위 CRUD, 스터디룸별 리뷰 목록"""

    def create(
        self,
        db: Session,
        reservation_id: int,
        data: ReviewCreate,
        current_user: User,
    ) -> Review:
        """
        예약에 대한 리뷰 작성.
        흐름: 예약 조회 → 없으면 404 → 본인 예약인지 403 → COMPLETED 여부 400 → 이미 리뷰 있으면 409 → 생성
        """
        reservation = reservation_repository.find_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다.",
            )
        if reservation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인의 예약에만 리뷰를 작성할 수 있습니다.",
            )
        if reservation.status != ReservationStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="완료된 예약(COMPLETED)에만 리뷰를 작성할 수 있습니다.",
            )
        existing = review_repository.find_by_reservation_id(db, reservation_id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="해당 예약에 이미 리뷰가 작성되어 있습니다.",
            )
        if not (1 <= data.rating <= 5) or (data.rating * 2) % 1 != 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="rating은 1~5 사이의 0.5 단위여야 합니다."
            )
        review = Review(
            reservation_id=reservation_id,
            user_id=current_user.id,
            rating=data.rating,
            comment=data.comment,
        )
        review_repository.save(db, review)
        db.commit()
        db.refresh(review)
        return review

    def get_by_reservation(
        self,
        db: Session,
        reservation_id: int,
        current_user: User,
    ) -> Review:
        """
        예약 단위 내 리뷰 조회.
        흐름: 예약 조회 → 404 → 본인 예약 403 → 리뷰 조회 → 없으면 404
        """
        reservation = reservation_repository.find_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다.",
            )
        if reservation.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인의 예약만 조회할 수 있습니다.",
            )
        review = review_repository.find_by_reservation_id(db, reservation_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 예약에 대한 리뷰가 없습니다.",
            )
        return review

    def update(
        self,
        db: Session,
        reservation_id: int,
        data: ReviewUpdate,
        current_user: User,
    ) -> Review:
        """
        예약에 대한 리뷰 수정.
        흐름: 예약 조회 → 404 → 리뷰 조회 → 404 → 본인 리뷰 403 → 수정 후 반환
        """
        reservation = reservation_repository.find_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다.",
            )
        review = review_repository.find_by_reservation_id(db, reservation_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 예약에 대한 리뷰가 없습니다.",
            )
        if review.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인의 리뷰만 수정할 수 있습니다.",
            )
        if data.rating is not None:
            review.rating = data.rating
        if data.comment is not None:
            review.comment = data.comment
        db.commit()
        db.refresh(review)
        return review

    def delete(
        self,
        db: Session,
        reservation_id: int,
        current_user: User,
    ) -> None:
        """
        예약에 대한 리뷰 삭제.
        흐름: 예약 조회 → 404 → 리뷰 조회 → 404 → 본인 리뷰 403 → 삭제
        """
        reservation = reservation_repository.find_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다.",
            )
        review = review_repository.find_by_reservation_id(db, reservation_id)
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 예약에 대한 리뷰가 없습니다.",
            )
        if review.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="본인의 리뷰만 삭제할 수 있습니다.",
            )
        review_repository.delete(db, review)
        db.commit()

    def get_by_studyroom(
        self,
        db: Session,
        room_id: int,
        limit: int = 20,
        offset: int = 0,
        sort: str | None = "recent",
    ) -> list[Review]:
        """
        스터디룸 전체 리뷰 조회 (예약과 무관, 1:N).
        흐름: 스터디룸 존재 확인 → 404 → 페이지네이션·정렬 후 목록 반환.
        """
        if db.get(StudyRoom, room_id) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="스터디룸을 찾을 수 없습니다.",
            )
        sort_recent = (sort or "").lower() == "recent"
        return review_repository.find_by_studyroom_id(
            db,
            studyroom_id=room_id,
            limit=max(1, min(100, limit)),
            offset=max(0, offset),
            sort_recent=sort_recent,
        )


review_service = ReviewService()
