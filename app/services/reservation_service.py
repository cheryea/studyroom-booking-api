# mysite4/services/reservation_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.reservation_repository import reservation_repository
from app.models import Reservation, StudyRoom, User
from app.schemas.reservation import ReservationCreate, ReservationStatus


class ReservationService:
    def create_reservation(
            self,
            db: Session,
            data: ReservationCreate,
            current_user: User
        ):
            # 1️⃣ 시작시간 < 종료시간 검증
            if data.start_datetime >= data.end_datetime:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="종료시간은 시작시간보다 이후여야 합니다."
                )

            # 2️⃣ 스터디룸 존재 확인
            studyroom = db.get(StudyRoom, data.studyroom_id)
            if not studyroom:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="해당 스터디룸이 존재하지 않습니다."
                )

            # 3️⃣ 시간 겹침 체크 (중요 🔥)
            existing = db.query(Reservation).filter(
                Reservation.studyroom_id == data.studyroom_id,
                Reservation.start_datetime < data.end_datetime,
                Reservation.end_datetime > data.start_datetime,
                Reservation.status == ReservationStatus.RESERVED
            ).first()

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="이미 해당 시간에 예약이 존재합니다."
                )

            # 4️⃣ 예약 생성
            new_reservation = Reservation(
                user=current_user,
                studyroom_id=data.studyroom_id,
                start_datetime=data.start_datetime,
                end_datetime=data.end_datetime,
                status=ReservationStatus.RESERVED
            )

            reservation_repository.save(db, new_reservation)

            db.commit()
            db.refresh(new_reservation)

            return new_reservation


    def get_my_reservations(self, db: Session, current_user: User):
        reservations = reservation_repository.find_by_user(
            db,
            current_user.id   # ⭐ 객체 말고 id 사용
        )

        if not reservations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="예약을 찾을 수 없습니다."
            )

        return reservations
    

reservation_service = ReservationService()