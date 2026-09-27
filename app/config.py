from functools import lru_cache
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    app_name: str = os.getenv("APP_NAME", "PocketSmart AI")
    secret_key: str = os.getenv("SECRET_KEY", "dev-only-secret-change-me")
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    database_path: Path = BASE_DIR / os.getenv("DATABASE_PATH", "data/pocketsmart.db")
    access_token_minutes: int = int(os.getenv("ACCESS_TOKEN_MINUTES", "120"))
    max_upload_mb: int = int(os.getenv("MAX_UPLOAD_MB", "5"))

@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.database_path.parent.mkdir(parents=True, exist_ok=True)
    return settings
