
from pydantic import BaseModel
from typing import Optional


# Dữ liệu khi tạo hồ sơ nhân viên
class EmployeeCreate(BaseModel):
    phone: str
    address: Optional[str] = None
    position: str


# Dữ liệu khi sửa hồ sơ nhân viên
class EmployeeUpdate(BaseModel):
    phone: Optional[str] = None
    address: Optional[str] = None
    position: Optional[str] = None


# Dữ liệu trả về
class EmployeeResponse(BaseModel):
    user_id: str
    full_name: str
    email: str
    phone: str
    address: Optional[str] = None
    position: str
