
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ServiceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)
    price: float = Field(gt=0, allow_inf_nan=False)
    duration_minutes: int = Field(gt=0, le=600)
    status: str = "active"


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None, min_length=1, max_length=100
    )
    description: Optional[str] = Field(
        default=None, min_length=1, max_length=1000
    )
    price: Optional[float] = Field(
        default=None, gt=0, allow_inf_nan=False
    )
    duration_minutes: Optional[int] = Field(
        default=None, gt=0, le=600
    )
    status: Optional[str] = None


class ServiceResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    service_id: str
    name: str
    description: str
    price: float
    duration_minutes: int
    status: str
