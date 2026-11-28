from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
from fastapi import HTTPException, Response

from app.users.repository import UserRepository
from app.users.schemas import CreateUser, UpdateUser

JWT_ALO = "HS256"
COOKIE_NAME = "access_token"
JWT_SECRET = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
REFRESH_TOKEN_EXPIRE_DAY = 30
COOKIE_EXPIRE = 900
ACCESS_TOKEN_EXPIRE_MINUTES = 15


class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def get_user(self, email: str):
        return self.repo.find_by_email(email)

    def login_user(self):
        pass

    def logout_user(self, user_id: str, res: Response):
        self.repo.clear_refresh_token(user_id)
        res.delete_cookie(
            key=COOKIE_NAME,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax",
        )

    def update_user(self, data: UpdateUser):
        return self.repo.update_user(data)

    def create_user(self, data: CreateUser, res: Response):
        if self.repo.find_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email already exist")

        user = self.repo.create_user(data)
        refresh_token = self.__create_jwt_token(
            user.id,
            user.email,
            datetime.now(UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAY),
        )
        access_token = self.__create_jwt_token(
            user.id,
            user.email,
            datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )

        # adding the fresh token
        self.repo.update_user(UpdateUser(refresh_token=refresh_token))

        res.set_cookie(
            key=COOKIE_NAME,
            value=access_token,
            path="/",
            secure=True,
            httponly=True,
            samesite="lax",
            max_age=COOKIE_EXPIRE,
        )

        return user

    # Private method for creating refresh token
    def __create_jwt_token(self, id: UUID | None, email: str, expire_at: datetime):
        token = jwt.encode(
            {
                "sub": {id, email},
                "exp": expire_at,
            },
            JWT_SECRET,
            JWT_ALO,
        )
        return token
