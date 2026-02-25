# app/schemas/review.py

from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional


class ReviewCreate(BaseModel):
    """리뷰 작성 요청 (POST /reservations/{reservation_id}/review)"""
    rating: float = Field(..., description="0~5 사이 점수")
    comment: Optional[str] = Field(
        None,
        min_length=0,
        max_length=500,
        description="리뷰 내용 (선택, 최대 500자)"
    )


class ReviewUpdate(BaseModel):
    """리뷰 수정 요청 (PUT /reservations/{reservation_id}/review)"""
    rating: Optional[float] = Field(None, description="평점 1~5")
    comment: Optional[str] = Field(
        None,
        min_length=0,
        max_length=500,
        description="리뷰 내용 (최대 500자)"
    )


class ReviewResponse(BaseModel):
    """리뷰 응답"""
    id: int
    reservation_id: int
    user_id: int
    rating: float
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
