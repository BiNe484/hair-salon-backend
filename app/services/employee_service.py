
from fastapi import HTTPException

from app.db.firebase import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(user_id: str, data: EmployeeCreate):
    db = get_db()

    # 1. Kiểm tra tài khoản có tồn tại không
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản"
        )

    user_data = user_doc.to_dict()

    # 2. Chỉ cho phép tài khoản có role employee
    if user_data.get("role") != "employee":
        raise HTTPException(
            status_code=400,
            detail="Tài khoản này không phải nhân viên"
        )

    # 3. Kiểm tra hồ sơ nhân viên đã tồn tại chưa
    employee_ref = db.collection("employees").document(user_id)

    if employee_ref.get().exists:
        raise HTTPException(
            status_code=409,
            detail="Hồ sơ nhân viên đã tồn tại"
        )

    # 4. Lưu hồ sơ vào Firestore
    employee_data = data.model_dump()
    employee_data["user_id"] = user_id

    employee_ref.set(employee_data)

    return {
        **employee_data,
        "full_name": user_data.get("full_name", ""),
        "email": user_data.get("email", ""),
    }


def get_all_employees():
    db = get_db()
    employee_docs = db.collection("employees").stream()

    employees = []

    for doc in employee_docs:
        employee_data = doc.to_dict()

        user_doc = db.collection("users").document(doc.id).get()
        user_data = user_doc.to_dict() if user_doc.exists else {}

        employees.append({
            **employee_data,
            "full_name": user_data.get("full_name", ""),
            "email": user_data.get("email", ""),
        })

    return employees


def get_employee(user_id: str):
    db = get_db()

    employee_doc = db.collection("employees").document(user_id).get()

    if not employee_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ nhân viên"
        )

    employee_data = employee_doc.to_dict()

    user_doc = db.collection("users").document(user_id).get()
    user_data = user_doc.to_dict() if user_doc.exists else {}

    return {
        **employee_data,
        "full_name": user_data.get("full_name", ""),
        "email": user_data.get("email", ""),
    }


def update_employee(user_id: str, data: EmployeeUpdate):
    db = get_db()

    employee_ref = db.collection("employees").document(user_id)

    if not employee_ref.get().exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ nhân viên"
        )

    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Chưa có thông tin cần cập nhật"
        )

    employee_ref.update(update_data)

    return get_employee(user_id)


def delete_employee(user_id: str):
    db = get_db()

    employee_ref = db.collection("employees").document(user_id)

    if not employee_ref.get().exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ nhân viên"
        )

    employee_ref.delete()

    return {
        "message": "Xóa hồ sơ nhân viên thành công",
        "user_id": user_id,
    }
