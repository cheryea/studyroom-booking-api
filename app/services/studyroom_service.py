# services/studyroom_service.py
from sqlalchemy.orm import Session
from app.repositories.studyroom_repository import studyroom_repository

class StudyRoomService:
    
    def read_studyrooms(self, db: Session, floor: int = None, min_capacity: int = None):
        return studyroom_repository.search(db, floor, min_capacity)



studyroom_service = StudyRoomService()