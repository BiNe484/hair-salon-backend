
from firebase_admin import auth
from firebase_admin import firestore

from app.db.firebase import get_db, initialize_firebase


def register_user(email: str, password: str, full_name: str):
    # 1. Khởi tạo Firebase
    initialize_firebase()

    # 2. Kiểm tra email đã tồn tại trong Firebase Authentication chưa
    try:
        auth.get_user_by_email(email)

        # Nếu tìm thấy tài khoản thì báo email đã được sử dụng
        raise ValueError("Email đã được đăng ký")

    except auth.UserNotFoundError:
        # Chưa có tài khoản thì tiếp tục đăng ký
        pass

    # 3. Tạo tài khoản Firebase Authentication
    firebase_user = auth.create_user(
        email=email,
        password=password,
        display_name=full_name,
    )

    uid = firebase_user.uid

    # 4. Lưu hồ sơ vào Firestore
    db = get_db()

    user_data = {
        "user_id": uid,
        "email": email,
        "full_name": full_name,
        "role": "customer",
        "status": "active",
    }

    db.collection("users").document(uid).set(user_data)

    return user_data
