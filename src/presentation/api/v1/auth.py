








from fastapi import APIRouter, Depends, Response, HTTPException, Request
from src.core.dependencies import get_user_service, get_current_user
from src.domain.services.user_service import UserService
from src.presentation.schemas.user import UserCreate, UserLogin
from src.core.config import settings
from src.core.auth import authx
from authx import RequestToken, TokenPayload

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register")
async def register_user(
    user_data: UserCreate,
    response: Response,
    user_service: UserService = Depends(get_user_service),
):
    """Регистрация нового пользователя"""
    try:
        user = await user_service.register(user_data.email, user_data.password)
        # Создаем JWT токены
        access_token = authx.create_access_token(uid=str(user.id))
        refresh_token = authx.create_refresh_token(uid=str(user.id))
        # Устанавливаем токены в cookies с помощью методов AuthX
        authx.set_access_cookies(access_token, response)
        authx.set_refresh_cookies(refresh_token, response)
        return {
            "message": "Регистрация прошла успешно",
            "user": {"id": user.id, "email": user.email}
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login_user(
    user_data: UserLogin,
    response: Response,
    user_service: UserService = Depends(get_user_service),
):
    """Вход пользователя"""
    try:
        tokens = await user_service.login(user_data.email, user_data.password)
        # Устанавливаем токены в cookies
        authx.set_access_cookies(tokens["access_token"], response)
        authx.set_refresh_cookies(tokens["refresh_token"], response)
        return {
            "message": "Вход выполнен успешно",
            "tokens": tokens
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(response: Response):
    """Выход пользователя"""
    # Удаляем токены из cookies
    authx.unset_cookies(response)
    return {"message": "Успешный выход"}

@router.post("/refresh")
async def refresh_access_token(
    response: Response,
    refresh_token: RequestToken = Depends(authx.get_refresh_token_from_request)
):
    """Обновление access-токена по refresh-токену"""
    try:
        # Проверяем и декодируем refresh-токен (verify_type=False, т.к. это не access-токен)
        payload: TokenPayload = authx.verify_token(token=refresh_token, verify_type=False)
        user_id = payload.sub  # `sub` содержит идентификатор пользователя (UID)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token payload")
        # Создаем новый access-токен
        new_access_token = authx.create_access_token(uid=user_id)
        # Обновляем access-токен в cookies
        authx.set_access_cookies(new_access_token, response)
        return {
            "message": "Токен обновлен успешно",
            "access_token": new_access_token
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")

@router.get("/me")
async def get_current_user_info(current_user=Depends(get_current_user)):
    """Получение информации о текущем пользователе"""
    return {
        "user": current_user,
        "message": "Authenticated successfully"
    }

@router.get("/protected")
async def protected_route(current_user=Depends(get_current_user)):
    """Пример защищенного маршрута"""
    return {
        "message": "Hello! This is a protected route.",
        "user": current_user
    }
