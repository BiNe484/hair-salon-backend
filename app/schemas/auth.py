
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("Mật khẩu phải có ít nhất 6 ký tự")
        return value

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value):
        if not value.strip():
            raise ValueError("Họ tên không được để trống")
        return value.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class AuthResponse(BaseModel):
    user_id: str
    email: EmailStr
    full_name: str
    role: str
    status: str
