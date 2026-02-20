# models/facility.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .studyroom_facility import StudyRoomFacility


class Facility(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    studyroom_facilities: Mapped[list["StudyRoomFacility"]] = relationship(
    back_populates="facility"
)
