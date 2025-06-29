from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Dating Portal"
    SECRET_KEY: str
    DATABASE_URL: str
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
