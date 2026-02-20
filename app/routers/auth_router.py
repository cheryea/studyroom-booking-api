# routers/auth_router.py

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(data: UserCreate, db: Session = Depends(get_db)):
    return auth_service.signup(db, data)


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    access_token = auth_service.login(db, data)
    return {"access_token": access_token}
