from fastapi import Depends
from sqlmodel import Session

from app.db.session import get_session
from app.users.repository import UserRepository
from app.users.service import UserService


def get_user_service(db: Session = Depends(get_session)):  # noqa: B008
    return UserService(UserRepository(db))
