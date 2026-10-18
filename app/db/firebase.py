import firebase_admin
from firebase_admin import credentials, firestore

from app.core.config import settings


def initialize_firebase():
    """Khởi tạo Firebase Admin SDK nếu chưa được khởi tạo."""

    try:
        return firebase_admin.get_app()
    except ValueError:
        pass

    service_account_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
    project_id = settings.FIREBASE_PROJECT_ID or None

    if service_account_path:
        # Dùng file service account JSON để xác thực
        cred = credentials.Certificate(service_account_path)

        options = {}
        if project_id:
            options["projectId"] = project_id

        return firebase_admin.initialize_app(
            cred,
            options or None
        )

    # Dùng Application Default Credentials nếu đã cấu hình
    options = {}
    if project_id:
        options["projectId"] = project_id

    return firebase_admin.initialize_app(
        options=options or None
    )


def get_db():
    """Trả về Firestore client để đọc và ghi dữ liệu."""

    initialize_firebase()
    return firestore.client()
