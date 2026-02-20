# repositories/studyroom_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.studyroom import StudyRoom

class StudyRoomRepository:
    # def save(self, db: Session, StudyRoom: StudyRoom):
    #     db.add(StudyRoom)
    #     return StudyRoom

    def find_all(self, db: Session):
        # select 문을 생성하고 scalars를 통해 결과 객체들을 리스트로 가져온다.
        stmt = select(StudyRoom)
        return db.scalars(stmt).all()

    # def find_by_name(self, db: Session, name: str):
    #     return db.scalar(select(StudyRoom).where(StudyRoom.name == name))


studyroom_repository = StudyRoomRepository()
