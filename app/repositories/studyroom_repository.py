# repositories/studyroom_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload
from app.models import StudyRoom, StudyRoomFacility

class StudyRoomRepository:

    def search(self, db: Session, floor: int = None, min_capacity: int = None):
        stmt = select(StudyRoom).options( selectinload(StudyRoom.studyroom_facilities) .selectinload(StudyRoomFacility.facility) )

        if floor is not None:
            stmt = stmt.where(StudyRoom.floor == floor)

        if min_capacity is not None:
            stmt = stmt.where(StudyRoom.capacity >= min_capacity)

        return db.scalars(stmt).all()


studyroom_repository = StudyRoomRepository()
