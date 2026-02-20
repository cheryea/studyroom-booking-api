# repositories/facility_repository.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.facility import Facility


class FacilityRepository:

    def find_all(self, db: Session):
        # scalars().all()을 사용하여 Facility 객체 리스트를 가져온다.
        return db.scalars(select(Facility)).all()

    def find_by_name(self, db: Session, name: str):
        return db.scalar(select(Facility).where(Facility.name == name))


facility_repository = FacilityRepository()
