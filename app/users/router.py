from fastapi import APIRouter, Depends, Response

from app.users.dependencies import get_user_service
from app.users.schemas import CreateUser, LoginUser, UpdateUser, UserData
from app.users.service import UserService

user_router = APIRouter()


@user_router.post("/sign-up", response_model=UserData)
def create_user(
    res: Response,
    data: CreateUser,
    service: UserService = Depends(get_user_service),  # noqa: B008
):
    return service.create_user(data, res)


@user_router.post("/sign-in", response_model=UserData)
def login_user(data: LoginUser, service: UserService = Depends(get_user_service)):  # noqa: B008
    pass


@user_router.post("/sign-out")
def sign_out():
    pass


@user_router.post("update-user", response_model=UserData)
def update_user(data: UpdateUser, service: UserService = Depends(get_user_service)):  # noqa: B008
    pass


@user_router.get("/", response_model=UserData)
def get_user():
    pass
