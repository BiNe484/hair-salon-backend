from app.db.firebase import get_db

try:
    db = get_db()

    # Thử đọc một collection trong Firestore
    db.collection("users").limit(1).get()

    print("Ket noi Firebase thanh cong!")

except Exception as e:
    print("Ket noi Firebase that bai!")
    print("Loi:", e)