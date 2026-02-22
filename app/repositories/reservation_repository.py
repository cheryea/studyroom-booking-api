# mysite4/repositories/reservation_repository.py

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.models.reservation import Reservation


class Reservation_Repository:
    def save(self, db: Session, new_reservation: Reservation):
        db.add(new_reservation)
        return new_reservation
    
    def find_by_user(self, db: Session, user_id: int):
        return db.scalars(
            select(Reservation)
            .options(
                joinedload(Reservation.studyroom)  # 스터디룸 미리 로딩
            )
            .where(Reservation.user_id == user_id)
            .order_by(Reservation.start_datetime.desc())  # 최신순
        ).all()



reservation_repository = Reservation_Repository()