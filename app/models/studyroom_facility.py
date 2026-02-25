# models/studyroom_facility.py

from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .studyroom import StudyRoom
    from .facility import Facility

class StudyRoomFacility(Base):
    __tablename__ = "studyroom_facilities"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # 각각 studyroom와 facility를 참조하는 외래키
    studyroom_id: Mapped[int] = mapped_column(ForeignKey("studyrooms.id"))
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id"))

    # 확장 데이터: 등록일 추가 가능
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    studyroom: Mapped["StudyRoom"] = relationship(
        back_populates="studyroom_facilities"
    )
    facility: Mapped["Facility"] = relationship(
        back_populates="studyroom_facilities"
    )