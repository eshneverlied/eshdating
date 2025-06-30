from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dating Portal"
    SECRET_KEY: str
    JWT_SECRET_KEY: str  # ⬅️ добавляем эту строку
    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
