
from fastapi import APIRouter

from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services.customer_service import (
    create_customer,
    get_all_customers,
    get_customer,
    update_customer,
    delete_customer,
)

router = APIRouter()


# 1. Tạo hồ sơ khách hàng
@router.post("/")
def create_customer_api(user_id: str, data: CustomerCreate):
    return create_customer(user_id, data)


# 2. Lấy danh sách khách hàng
@router.get("/")
def get_all_customers_api():
    return get_all_customers()


# 3. Lấy thông tin một khách hàng
@router.get("/{user_id}")
def get_customer_api(user_id: str):
    return get_customer(user_id)


# 4. Cập nhật thông tin khách hàng
@router.patch("/{user_id}")
def update_customer_api(user_id: str, data: CustomerUpdate):
    return update_customer(user_id, data)


# 5. Xóa hồ sơ khách hàng
@router.delete("/{user_id}")
def delete_customer_api(user_id: str):
    return delete_customer(user_id)
