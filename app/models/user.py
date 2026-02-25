# app/models/user.py

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import Reservation
    from .review import Review


class User(Base):
    __tablename__ = "users"  # 테이블 이름

    id: Mapped[int] = mapped_column(
        primary_key=True,      # 기본 키
        autoincrement=True     # 자동 증가
    )

    student_number: Mapped[str] = mapped_column(
        String(20),           # 최대 20자
        unique=True,           # 중복 불가
        index=True,          # 인덱스 생성
        nullable=False         # 값 필수(null 불가)
    )

    name: Mapped[str] = mapped_column(
        String(50),            # 최대 50자
        nullable=False         # 값 필수(null 불가)
    )

    password: Mapped[str] = mapped_column(
        String(200),           # 비밀번호 해시 저장
        nullable=False
    )

    reservations: Mapped[list["Reservation"]] = relationship(
        "Reservation", back_populates="user"
    )
    reviews: Mapped[list["Review"]] = relationship(
        "Review", back_populates="user"
    )