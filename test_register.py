
from app.services.auth_service import register_user

try:
    result = register_user(
        email="test.customer.001@example.com",
        password="TestPass123!",
        full_name="Khach hang thu nghiem",
    )

    print("Dang ky thanh cong!")
    print("Du lieu:", result)

except Exception as e:
    print("Dang ky that bai!")
    print("Loi:", e)
