# app/repositories/review_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, desc

from app.models.review import Review
from app.models.reservation import Reservation


class ReviewRepository:
    """리뷰 DB 접근 레이어"""

    def find_by_reservation_id(self, db: Session, reservation_id: int) -> Review | None:
        """예약 ID로 리뷰 1건 조회 (예약당 리뷰 1:1)"""
        return db.scalars(
            select(Review).where(Review.reservation_id == reservation_id)
        ).first()

    def find_by_id(self, db: Session, review_id: int) -> Review | None:
        """리뷰 ID로 조회"""
        return db.get(Review, review_id)

    def save(self, db: Session, review: Review) -> Review:
        """리뷰 저장"""
        db.add(review)
        return review

    def delete(self, db: Session, review: Review) -> None:
        """리뷰 삭제"""
        db.delete(review)

    def find_by_studyroom_id(
        self,
        db: Session,
        studyroom_id: int,
        limit: int = 20,
        offset: int = 0,
        sort_recent: bool = True,
    ) -> list[Review]:
        """스터디룸별 리뷰 목록 (예약 join, 페이지네이션·정렬)"""
        q = (
            select(Review)
            .join(Reservation, Review.reservation_id == Reservation.id)
            .where(Reservation.studyroom_id == studyroom_id)
            .options(joinedload(Review.reservation), joinedload(Review.user))
        )
        if sort_recent:
            q = q.order_by(desc(Review.created_at))
        q = q.limit(limit).offset(offset)
        return list(db.scalars(q).all())


review_repository = ReviewRepository()
