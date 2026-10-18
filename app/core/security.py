
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from app.db.firebase import get_db


# Đọc token từ request
bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
):
    # Bước 1: Kiểm tra người dùng có gửi token không
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token",
        )

    token = credentials.credentials

    # Bước 2: Kiểm tra token bằng Firebase Authentication
    try:
        decoded_token = auth.verify_id_token(token)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from exc

    # Bước 3: Lấy UID từ token
    uid = decoded_token.get("uid")

    if not uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )

    # Bước 4: Tìm hồ sơ người dùng trong Firestore
    db = get_db()
    user_doc = db.collection("users").document(uid).get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User profile not found",
        )

    user_data = user_doc.to_dict()

    # Bước 5: Kiểm tra tài khoản còn hoạt động không
    if user_data.get("status", "active") != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return {
        "uid": uid,
        **user_data,
    }


def require_roles(*allowed_roles: str):
    # Tạo bộ kiểm tra quyền theo vai trò
    def role_checker(
        current_user: dict = Depends(get_current_user),
    ):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission",
            )

        return current_user

    return role_checker
