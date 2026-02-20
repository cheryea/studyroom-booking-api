# services/facility_service.py
from sqlalchemy.orm import Session
from app.repositories.facility_repository import facility_repository


class FacilityService:

    def read_facilities(self, db: Session):
        return facility_repository.find_all(db)


facility_service = FacilityService()
