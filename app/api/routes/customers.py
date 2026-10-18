
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_customers():
    return {"message": "Customers API is running"}
