# app/models/reservation.py

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, Enum, func
from datetime import datetime
import enum
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .studyroom import StudyRoom
    from .review import Review

# 예약 상태 Enum
class ReservationStatus(str, enum.Enum):
    RESERVED = "RESERVED"
    CANCELED = "CANCELED"
    COMPLETED = "COMPLETED"

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    studyroom_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("studyrooms.id", ondelete="CASCADE"),
        nullable=False
    )

    start_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus),
        default=ReservationStatus.RESERVED,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    # 관계 설정
    user: Mapped["User"] = relationship("User", back_populates="reservations")
    studyroom: Mapped["StudyRoom"] = relationship("StudyRoom", back_populates="reservations")
    review: Mapped["Review"] = relationship("Review", back_populates="reservation")
