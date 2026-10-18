from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import RegisterRequest
from app.services.auth_service import register_user


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    try:
        return register_user(
            email=data.email,
            password=data.password,
            full_name=data.full_name,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không thể đăng ký tài khoản",
        ) from exc
