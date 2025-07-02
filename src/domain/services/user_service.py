# from src.domain.entities.user import User
# from src.domain.repositories.user_repository import UserRepository
# from passlib.context import CryptContext
# from datetime import datetime
# from fastapi import HTTPException
# from authx import AuthX, AuthXConfig
# from src.core.config import settings

# class UserService:
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
#         self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#         config = AuthXConfig(
#             JWT_SECRET_KEY=settings.JWT_SECRET_KEY,   # обязательно
#             JWT_ALGORITHM="HS256",
#             JWT_ACCESS_TOKEN_EXPIRES=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # seconds
#         )
#         self.authx = AuthX(config=config)

#     async def register(self, email: str, password: str) -> User:
#         existing_user = await self.user_repository.get_by_email(email)
#         if existing_user:
#             raise ValueError("Email already registered")

#         password_hash = self.pwd_context.hash(password)
#         user = User(
#             id=0,
#             email=email,
#             password_hash=password_hash,
#             created_at=datetime.utcnow(),
#         )
#         return await self.user_repository.create(user)

#     async def login(self, email: str, password: str) -> dict:
#         user = await self.user_repository.get_by_email(email)
#         if not user or not self.pwd_context.verify(password, user.password_hash):
#             raise HTTPException(status_code=401, detail="Invalid email or password")

#         token = self.authx.create_access_token(
#             uid=str(user.id),
#             additional_data={"email": user.email}
#         )
#         return {"access_token": token, "token_type": "bearer"}





from fastapi import HTTPException
from src.core.config import settings
from src.domain.entities.user import User
from datetime import datetime

class UserService:
    def __init__(self, user_repository, authx, pwd_context):
        self.user_repository = user_repository
        self.authx = authx
        self.pwd_context = pwd_context

    async def register(self, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = self.pwd_context.hash(password)
        return await self.user_repository.create(email=email, password_hash=hashed_password)

    async def login(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_by_email(email)
        if not user or not self.pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        access_token = self.authx.create_access_token(
            uid=str(user.id),
            additional_data={"email": user.email},
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        refresh_token = self.authx.create_refresh_token(
            uid=str(user.id),
            additional_data={"email": user.email},
            expires_in=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_access_token(self, refresh_payload: dict) -> dict:
        user = await self.user_repository.get_by_id(int(refresh_payload["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        access_token = self.authx.create_access_token(
            uid=refresh_payload["sub"],
            additional_data={"email": refresh_payload["email"]},
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_payload["jti"],  # Сохраняем тот же refresh-токен
            "token_type": "bearer",
        }
