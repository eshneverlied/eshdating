from fastapi import FastAPI
from src.core.config import settings
from src.core.logging import setup_logging
from src.presentation.api.v1.auth import router as auth_router
from authx import AuthX

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/api/docs",
)

authx = AuthX()  # Убираем secret_key
# app.add_middleware(authx.middleware)  # Раскомментируйте позже, если нужно

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
