
from fastapi import APIRouter

from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.services.employee_service import (
    create_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee,
)

router = APIRouter()


@router.post("/")
def create_employee_api(user_id: str, data: EmployeeCreate):
    return create_employee(user_id, data)


@router.get("/")
def get_all_employees_api():
    return get_all_employees()


@router.get("/{user_id}")
def get_employee_api(user_id: str):
    return get_employee(user_id)


@router.patch("/{user_id}")
def update_employee_api(user_id: str, data: EmployeeUpdate):
    return update_employee(user_id, data)


@router.delete("/{user_id}")
def delete_employee_api(user_id: str):
    return delete_employee(user_id)
