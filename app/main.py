
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import auth, users, customers, employees, services

app = FastAPI(
    title="Hair Salon API",
    description="API quản lý hệ thống Hair Salon",
    version="1.0.0"
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # Lấy lỗi đầu tiên
    first_error = exc.errors()[0]

    message = first_error["msg"]

    # Xóa chữ "Value error, " nếu có
    if message.startswith("Value error, "):
        message = message.replace("Value error, ", "", 1)

    return JSONResponse(
        status_code=422,
        content={"detail": message}
    )

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(services.router, prefix="/services", tags=["Services"])


@app.get("/")
def home():
    return {"message": "Hair Salon API is running"}
