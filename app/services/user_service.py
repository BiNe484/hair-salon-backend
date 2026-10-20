
from fastapi import HTTPException
from firebase_admin import auth

from app.db.firebase import get_db
from app.schemas.user import UserUpdate


def get_all_users():
    db = get_db()
    user_docs = db.collection("users").stream()

    users = []

    for doc in user_docs:
        user_data = doc.to_dict() or {}

        users.append({
            **user_data,
            "user_id": user_data.get("user_id", doc.id),
            "status": user_data.get("status", "active"),
        })

    return users


def get_user(user_id: str):
    db = get_db()

    user_doc = db.collection("users").document(user_id).get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản",
        )

    user_data = user_doc.to_dict() or {}

    return {
        **user_data,
        "user_id": user_data.get("user_id", user_id),
        "status": user_data.get("status", "active"),
    }


def update_user(user_id: str, data: UserUpdate):
    db = get_db()

    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản",
        )

    user_data = user_doc.to_dict() or {}
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Chưa có thông tin cần cập nhật",
        )

    # Không cho phép email rỗng hoặc chỉ chứa khoảng trắng
    if "email" in update_data:
        email = str(update_data["email"]).strip()

        if not email:
            raise HTTPException(
                status_code=400,
                detail="Email không được để trống",
            )

        update_data["email"] = email

    # Đồng bộ thông tin với Firebase Authentication
    try:
        firebase_updates = {}

        if "email" in update_data:
            firebase_updates["email"] = update_data["email"]

        if "full_name" in update_data:
            full_name = update_data["full_name"].strip()

            if not full_name:
                raise HTTPException(
                    status_code=400,
                    detail="Họ tên không được để trống",
                )

            update_data["full_name"] = full_name
            firebase_updates["display_name"] = full_name

        if firebase_updates:
            auth.update_user(user_id, **firebase_updates)

    except auth.EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=409,
            detail="Email đã được tài khoản khác sử dụng",
        ) from exc
    except auth.UserNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản trong Firebase Authentication",
        ) from exc

    # Chỉ cập nhật các trường được cho phép trong UserUpdate
    user_ref.update(update_data)

    return get_user(user_id)
