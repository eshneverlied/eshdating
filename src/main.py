# from dotenv import load_dotenv
# load_dotenv()
# from fastapi import FastAPI
# from src.core.config import settings
# from src.core.logging import setup_logging
# from src.core.dependencies import get_current_user
# from src.presentation.api.v1.auth import router as auth_router
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
# from fastapi.requests import Request

# from fastapi import Depends, HTTPException

# from authx import AuthX
# setup_logging()
# templates = Jinja2Templates(directory="templates")


# authx = AuthX()

# app = FastAPI(
#     title=settings.PROJECT_NAME,
#     version="1.0.0",
#     docs_url="/api/docs",
# )

# # app.add_middleware(authx.middleware)  # если будет использоваться

# # передаём authx через зависимость
# app.state.authx = authx

# app.include_router(auth_router, prefix="/api/v1/auth")
# app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.get("/")
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

# @app.get("/dashboard")
# async def dashboard(request: Request, user=Depends(get_current_user)):
#     return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})





from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.core.config import settings
from src.core.logging import setup_logging
from src.core.dependencies import get_current_user, get_csrf_token
from src.presentation.api.v1.auth import router as auth_router

setup_logging()
templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/api/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth", tags=["Auth"])
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def index(request: Request, response: Response):
    csrf_token = request.cookies.get("csrf_token") or get_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,  # Allow cross-origin cookie
    )
    return {"csrf_token": csrf_token}
