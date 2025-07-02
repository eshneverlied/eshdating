# from fastapi import APIRouter, HTTPException, Depends,status
# from src.domain.services.user_service import UserService
# from src.presentation.schemas.user import UserCreate, User, UserLogin, Token
# from src.core.dependencies import get_user_service
# from fastapi.responses import JSONResponse
# router = APIRouter()

# @router.post("/register", response_model=User)
# async def register_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
#     try:
#         user = await user_service.register(user_data.email, user_data.password)
#         return user
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/login", response_model=Token)
# async def login_user(user_data: UserLogin, user_service: UserService = Depends(get_user_service)):
#     try:
#         token = await user_service.login(user_data.email, user_data.password)
#         return token
#     except HTTPException as e:
#         raise e

# @router.post("/logout", status_code=200, tags=["Auth"])
# async def logout_user():
#     """
#     Информирует клиент, что токен нужно удалить
#     !!!ПЕРЕДЕЛАТЬ С REDIS!!!
#     """
#     return JSONResponse(
#         content={"message": "Successfully logged out. Please delete your token on the client side."},
#         status_code=status.HTTP_200_OK
#     )

from fastapi import APIRouter, Depends, Response, HTTPException, Request
from src.core.dependencies import get_user_service, get_current_user, get_refresh_token, get_csrf_token
from src.domain.services.user_service import UserService
from src.presentation.schemas.user import UserCreate, UserLogin, Token, User
from src.core.config import settings

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=User)
async def register_user(
    user_data: UserCreate,
    response: Response,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    csrf_token = request.headers.get("X-CSRF-Token") or get_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,
    )
    user = await user_service.register(user_data.email, user_data.password)
    access_token = user_service.authx.create_access_token(
        uid=str(user.id),
        additional_data={"email": user.email},
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    refresh_token = user_service.authx.create_refresh_token(
        uid=str(user.id),
        additional_data={"email": user.email},
        expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        domain=None,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,
    )
    return user

@router.post("/login", response_model=Token)
async def login_user(
    user_data: UserLogin,
    response: Response,
    request: Request,
    user_service: UserService = Depends(get_user_service),
):
    csrf_token = request.headers.get("X-CSRF-Token") or get_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,
    )
    tokens = await user_service.login(user_data.email, user_data.password)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        domain=None,
    )
    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,
    )
    return tokens

@router.post("/refresh", response_model=Token)
async def refresh_token(
    response: Response,
    request: Request,
    refresh_payload: dict = Depends(get_refresh_token),
    user_service: UserService = Depends(get_user_service),
):
    csrf_token = request.headers.get("X-CSRF-Token") or get_csrf_token()
    response.set_cookie(
        key="csrf_token",
        value=csrf_token,
        httponly=False,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
        domain=None,
    )
    tokens = await user_service.refresh_access_token(refresh_payload)
    response.set_cookie(
        key="access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,  # True in production
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        path="/",
        domain=None,
    )
    return tokens

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", path="/", domain=None)
    response.delete_cookie("refresh_token", path="/", domain=None)
    response.delete_cookie("csrf_token", path="/", domain=None)
    return {"message": "Logged out successfully"}
