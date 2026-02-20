# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Review
class ReviewCreate(BaseModel):
    reservation_id: int
    rating: int = Field(..., ge=1, le=5)  # 1~5 제한
    comment: Optional[str] = Field(
        None,
        min_length=5,
        max_length=500
    )

class ReviewResponse(BaseModel):
    id: int
    reservation_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    # class Config:
    #     orm_mode = True
