
from fastapi import HTTPException

from app.db.firebase import get_db
from app.schemas.service import ServiceCreate, ServiceUpdate


VALID_STATUSES = {"active", "inactive"}


def validate_status(status: str):
    if status not in VALID_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Trạng thái chỉ được là 'active' hoặc 'inactive'",
        )


def create_service(data: ServiceCreate):
    db = get_db()

    # Kiểm tra trạng thái dịch vụ
    validate_status(data.status)

    # Tạo ID tự động cho dịch vụ
    service_ref = db.collection("services").document()
    service_id = service_ref.id

    # Chuẩn bị dữ liệu
    service_data = data.model_dump()
    service_data["service_id"] = service_id

    # Lưu vào Firestore
    service_ref.set(service_data)

    return service_data


def get_all_services():
    db = get_db()

    service_docs = db.collection("services").stream()
    services = []

    for doc in service_docs:
        service_data = doc.to_dict()
        services.append(service_data)

    return services


def get_service(service_id: str):
    db = get_db()

    service_ref = db.collection("services").document(service_id)
    service_doc = service_ref.get()

    if not service_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy dịch vụ",
        )

    return service_doc.to_dict()


def update_service(service_id: str, data: ServiceUpdate):
    db = get_db()

    service_ref = db.collection("services").document(service_id)
    service_doc = service_ref.get()

    if not service_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy dịch vụ",
        )

    # Chỉ lấy các trường được gửi lên
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Chưa có thông tin cần cập nhật",
        )

    # Kiểm tra trạng thái nếu có cập nhật
    if "status" in update_data:
        validate_status(update_data["status"])

    # Lưu thay đổi
    service_ref.update(update_data)

    return get_service(service_id)


def delete_service(service_id: str):
    db = get_db()

    service_ref = db.collection("services").document(service_id)
    service_doc = service_ref.get()

    if not service_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy dịch vụ",
        )

    service_ref.delete()

    return {
        "message": "Xóa dịch vụ thành công",
        "service_id": service_id,
    }
