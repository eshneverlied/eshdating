from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dating Portal"
    SECRET_KEY: str
    JWT_SECRET_KEY: str  # ⬅️ добавляем эту строку
    DATABASE_URL: str
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:8000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TG_SESSION_DIR: str = "sessions"


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
