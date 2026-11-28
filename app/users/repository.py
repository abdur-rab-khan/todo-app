from pwdlib import PasswordHash
from sqlmodel import Column, Session, select

from app.users.models import User
from app.users.schemas import CreateUser, UpdateUser


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str):
        return self.db.exec(select(User).where(Column(email) == email)).one()

    def create_user(self, data: CreateUser):
        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(data.password)

        user = User(
            email=data.email,
            dob=data.dob,
            first_name=data.first_name,
            last_name=data.last_name,
            password=hashed_password,
            profile_url=data.profile_url,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def clear_refresh_token(self, user_id: str):
        user = self.db.exec(select(User).where(id == user_id)).one()
        user.refresh_token = None
        self.db.add(user)
        self.db.commit()

    def update_user(self, data: UpdateUser):
        pass
