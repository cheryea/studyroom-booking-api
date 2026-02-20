# mysite4/routers/user_router.py
from fastapi import APIRouter, Depends
from app.schemas.user import UserResponse

from app.models.user import User
from dependencies import get_current_user


router = APIRouter(tags=["Users"])


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
