
from pydantic import BaseModel
from typing import Optional


# Dữ liệu khi tạo hồ sơ khách hàng
class CustomerCreate(BaseModel):
    phone: str
    address: Optional[str] = None


# Dữ liệu khi sửa hồ sơ khách hàng
class CustomerUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None


# Dữ liệu trả về
class CustomerResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: str
    address: Optional[str] = None
    rank: str = "brown"
    points: int = 0
