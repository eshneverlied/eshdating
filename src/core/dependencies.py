




from fastapi import Request, HTTPException, Depends
from src.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.infrastructure.database.repositories.telegram_session_repository import (
    SQLAlchemyTelegramSessionRepository,
)
from src.infrastructure.database.session import get_db_session
from passlib.context import CryptContext
from src.domain.services.user_service import UserService
from src.domain.services.telegram_session_service import TelegramSessionService
from authx import TokenPayload
from src.core.auth import authx  # Импортируем уже настроенный AuthX

# Контекст для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_service(session=Depends(get_db_session)) -> UserService:
    """
    Создаем сервис пользователей
    """
    return UserService(
        SQLAlchemyUserRepository(session),
        authx=authx,
        pwd_context=pwd_context
    )


def get_telegram_session_service(
    session=Depends(get_db_session),
) -> TelegramSessionService:
    """Создаем сервис телеграм-сессий."""
    return TelegramSessionService(
        SQLAlchemyTelegramSessionRepository(session)
    )

async def get_current_user(
    payload: TokenPayload = Depends(authx.access_token_required),  # проверяет access-токен и возвращает его payload
    user_service: UserService = Depends(get_user_service)
):
    """
    Проверяет токен пользователя и возвращает информацию о текущем пользователе.
    """
    # После успешной верификации токена мы получаем объект TokenPayload
    # Поле `sub` содержит UID пользователя (т.к. при создании токена мы передавали uid=str(user.id))
    try:
        user_id = payload.sub
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        # Получаем пользователя из базы данных по ID
        user = await user_service.get_user_by_id(int(user_id))
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {str(e)}")
    # Возвращаем только необходимые данные о пользователе
    return {"id": user.id, "email": user.email}
