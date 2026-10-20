
from fastapi import APIRouter

from app.schemas.user import UserUpdate, UserResponse
from app.services.user_service import (
    get_all_users,
    get_user,
    update_user,
)

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
def get_users():
    return get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user_api(user_id: str):
    return get_user(user_id)


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_api(user_id: str, data: UserUpdate):
    return update_user(user_id, data)
