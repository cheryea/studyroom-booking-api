# app/models/studyroom.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import Reservation

class StudyRoom(Base):
    __tablename__ = "studyrooms"  # 테이블 이름

    id: Mapped[int] = mapped_column(
        primary_key=True,      # 기본 키
        autoincrement=True     # 자동 증가
    )

    name: Mapped[str] = mapped_column(
        String(50),            # 스터디룸 이름, 최대 50자
        nullable=False
    )

    floor: Mapped[int] = mapped_column(
        Integer,               # 층 정보
        nullable=False
    )

    capacity: Mapped[int] = mapped_column(
        Integer,               # 최대 수용 인원
        nullable=False
    )

    location: Mapped[str] = mapped_column(
        String(100),           # 위치 설명, 최대 100자
        nullable=False
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        "Reservation", back_populates="studyroom"
    )