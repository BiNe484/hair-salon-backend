
from fastapi import APIRouter

from app.schemas.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
)
from app.services.service_service import (
    create_service,
    get_all_services,
    get_service,
    update_service,
    delete_service,
)

router = APIRouter()


@router.post("/", response_model=ServiceResponse, status_code=201)
def create_service_api(data: ServiceCreate):
    return create_service(data)


@router.get("/", response_model=list[ServiceResponse])
def get_all_services_api():
    return get_all_services()


@router.get("/{service_id}", response_model=ServiceResponse)
def get_service_api(service_id: str):
    return get_service(service_id)


@router.patch("/{service_id}", response_model=ServiceResponse)
def update_service_api(service_id: str, data: ServiceUpdate):
    return update_service(service_id, data)


@router.delete("/{service_id}")
def delete_service_api(service_id: str):
    return delete_service(service_id)
