from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from src.core.config import settings
from src.core.logging import setup_logging
from src.presentation.api.v1.auth import router as auth_router


from authx import AuthX
setup_logging()

authx = AuthX()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/api/docs",
)

# app.add_middleware(authx.middleware)  # если будет использоваться

# передаём authx через зависимость
app.state.authx = authx

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
