# app/schemas/user.py
from pydantic import BaseModel, Field

# User
class UserCreate(BaseModel):
    student_number: str = Field(..., max_length=20, description="학번")
    password: str = Field(..., min_length=4, description="비밀번호")
    name: str = Field(..., max_length=50, description="사용자 이름")

class UserResponse(BaseModel):
    id: int
    student_number: str
    name: str

    # class Config:
    #     orm_mode = True

class UserLogin(BaseModel):
    student_number: str = Field(..., max_length=20, description="학번")
    password: str = Field(..., min_length=4, description="비밀번호")

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"