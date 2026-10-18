
from pydantic import BaseModel, EmailStr
from typing import Optional


# Dữ liệu dùng khi tạo tài khoản
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    role: str = "customer"


# Dữ liệu dùng khi cập nhật tài khoản
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None


# Dữ liệu API trả về
class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    role: str
    status: str = "active"
