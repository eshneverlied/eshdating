from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.dependencies import get_current_user
from src.presentation.api.v1.auth import router as auth_router
from src.presentation.api.v1.telegram import router as telegram_router
from src.core.auth import authx

# Создаем приложение
app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url="/api/docs"
)

# Добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,  # Важно для cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Инициализируем AuthX с приложением
# Инициализация обработчиков ошибок AuthX
authx.handle_errors(app)

# Статические файлы и шаблоны
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Подключаем роутеры
app.include_router(auth_router)
app.include_router(telegram_router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard")
async def dashboard(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
# Добавьте этот endpoint в ваш auth router
