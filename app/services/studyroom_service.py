# services/studyroom_service.py
from sqlalchemy.orm import Session
from app.repositories.studyroom_repository import studyroom_repository

class StudyRoomService:
    # def create_tag(self, db: Session, data: TagCreate):
    #     with db.begin():
    #         # 1. 이미 존재하는 태그인지 확인
    #         existing_tag = tag_repository.find_by_name(db, data.name)
    #         if existing_tag:
    #             raise HTTPException(
    #                 status_code=400, detail="이미 존재하는 태그 이름입니다."
    #             )

    #         # 2. 태그 생성 및 저장
    #         new_tag = Tag(name=data.name)

    #         tag_repository.save(db, new_tag)

    #     db.refresh(new_tag)
    #     return new_tag

    def read_studyrooms(self, db: Session, floor: int = None, min_capacity: int = None):
        return studyroom_repository.search(db, floor, min_capacity)



studyroom_service = StudyRoomService()