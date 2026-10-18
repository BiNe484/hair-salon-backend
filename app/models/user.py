
from typing import Optional
from datetime import datetime


class User:
    def __init__(
        self,
        user_id: str,
        email: str,
        full_name: str,
        role: str = "customer",
        status: str = "active",
        created_at: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.email = email
        self.full_name = full_name
        self.role = role
        self.status = status
        self.created_at = created_at

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "status": self.status,
            "created_at": self.created_at,
        }
