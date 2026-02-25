# app/models/review.py

from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime, CheckConstraint, func
from database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .reservation import Reservation
    from .user import User


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )

    reservation_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("reservations.id", ondelete="CASCADE"),
        unique=True,  # 한 예약당 리뷰 1개만
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    rating: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    comment: Mapped[str] = mapped_column(
        String(500),  # 리뷰 내용, 최대 500자
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # 관계
    reservation: Mapped["Reservation"] = relationship("Reservation", back_populates="review")
    user: Mapped["User"] = relationship("User", back_populates="reviews")
