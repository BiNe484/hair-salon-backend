
from fastapi import HTTPException
from app.db.firebase import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate


def create_customer(user_id: str, data: CustomerCreate):
    db = get_db()

    # Kiểm tra tài khoản có tồn tại không
    user_ref = db.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy tài khoản"
        )

    user_data = user_doc.to_dict()

    # Chỉ tài khoản khách hàng mới có hồ sơ customer
    if user_data.get("role") != "customer":
        raise HTTPException(
            status_code=400,
            detail="Tài khoản này không phải khách hàng"
        )

    customer_ref = db.collection("customers").document(user_id)

    # Không tạo trùng hồ sơ
    if customer_ref.get().exists:
        raise HTTPException(
            status_code=409,
            detail="Hồ sơ khách hàng đã tồn tại"
        )

    customer_data = data.model_dump()
    customer_data["user_id"] = user_id

    customer_ref.set(customer_data)

    return {
        "user_id": user_id,
        "full_name": user_data.get("full_name", ""),
        "email": user_data.get("email", ""),
        **customer_data,
    }


def get_all_customers():
    db = get_db()
    customer_docs = db.collection("customers").stream()

    customers = []

    for doc in customer_docs:
        customer_data = doc.to_dict()

        # Lấy thông tin tài khoản từ collection users
        user_doc = db.collection("users").document(doc.id).get()
        user_data = user_doc.to_dict() if user_doc.exists else {}

        customers.append({
            **customer_data,
            "full_name": user_data.get("full_name", ""),
            "email": user_data.get("email", ""),
        })

    return customers


def get_customer(user_id: str):
    db = get_db()

    customer_doc = (
        db.collection("customers")
        .document(user_id)
        .get()
    )

    if not customer_doc.exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ khách hàng"
        )

    customer_data = customer_doc.to_dict()

    user_doc = db.collection("users").document(user_id).get()
    user_data = user_doc.to_dict() if user_doc.exists else {}

    return {
        **customer_data,
        "full_name": user_data.get("full_name", ""),
        "email": user_data.get("email", ""),
    }


def update_customer(user_id: str, data: CustomerUpdate):
    db = get_db()

    customer_ref = db.collection("customers").document(user_id)

    if not customer_ref.get().exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ khách hàng"
        )

    # Chỉ lấy những trường được gửi lên
    update_data = data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Chưa có thông tin cần cập nhật"
        )

    customer_ref.update(update_data)

    return get_customer(user_id)


def delete_customer(user_id: str):
    db = get_db()

    customer_ref = db.collection("customers").document(user_id)

    if not customer_ref.get().exists:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy hồ sơ khách hàng"
        )

    customer_ref.delete()

    return {
        "message": "Xóa hồ sơ khách hàng thành công",
        "user_id": user_id,
    }
