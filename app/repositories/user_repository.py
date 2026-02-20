# repositories/user_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User


class UserRepository:
    def save(self, db: Session, user: User):
        db.add(user)
        return user

    def find_by_student_number(self, db: Session, student_number: str):
        stmt = select(User).where(User.student_number == student_number)
        return db.scalars(stmt).first()

    def find_by_id(self, db: Session, user_id: int):
        return db.get(User, user_id)


user_repository = UserRepository()
