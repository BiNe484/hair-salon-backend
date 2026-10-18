
import os
from pathlib import Path

from dotenv import load_dotenv

# Tìm thư mục gốc của project
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Đọc các biến trong file .env
load_dotenv(PROJECT_ROOT / ".env")


class Settings:
    APP_NAME = os.getenv("APP_NAME", "Hair Salon API")
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_SERVICE_ACCOUNT_PATH = os.getenv(
        "FIREBASE_SERVICE_ACCOUNT_PATH", ""
    )


settings = Settings()
