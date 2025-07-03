

from fastapi import HTTPException
from src.domain.entities.user import User
from datetime import datetime
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

class UserService:
    def __init__(self, user_repository, authx, pwd_context):
        self.user_repository = user_repository
        self.authx = authx
        self.pwd_context = pwd_context

    async def register(self, email: str, password: str) -> User:
        """Регистрация нового пользователя"""
        # Проверяем, существует ли пользователь
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Хешируем пароль
        hashed_password = self.pwd_context.hash(password)

        # Создаем пользователя с правильными полями для PostgreSQL
        user = User(
            id=0,  # PostgreSQL автоматически присвоит ID при создании
            email=email,
            password_hash=hashed_password,
            created_at=datetime.utcnow()
        )

        created_user = await self.user_repository.create(user)
        return created_user

    async def login(self, email: str, password: str) -> dict:
        """Вход пользователя"""
        # Находим пользователя по email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Проверяем пароль
        if not self.pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Создаем токены
        try:
            access_token = self.authx.create_access_token(
                uid=str(user.id),
                additional_data={"email": user.email}  # Добавляем email как в оригинале
            )
            refresh_token = self.authx.create_refresh_token(uid=str(user.id))

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_id": user.id,
                "email": user.email
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating tokens: {str(e)}")

    async def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def refresh_token(self, refresh_token: str) -> dict:
            """Обновление access токена по refresh токену (если вызывается вне FastAPI)."""
            try:
                # Декодируем JWT (проверяем подпись и срок действия)
                payload = jwt.decode(
                    refresh_token,
                    self.authx.config.JWT_SECRET_KEY,
                    algorithms=[self.authx.config.JWT_ALGORITHM]
                )
                user_id = int(payload.get("sub") or payload.get("uid") or 0)
                user = await self.get_user_by_id(user_id)
                # Генерируем новый access-токен с тем же UID
                new_access = self.authx.create_access_token(uid=str(user.id), additional_data={"email": user.email})
                return {"access_token": new_access, "token_type": "bearer"}
            except ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Refresh token expired")
            except InvalidTokenError as e:
                raise HTTPException(status_code=401, detail=f"Invalid refresh token: {e}")
