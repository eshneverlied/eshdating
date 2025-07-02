from fastapi import Depends, HTTPException, Request
from src.domain.services.user_service import UserService
from src.infrastructure.database.repositories.user_repository import UserRepository
from src.infrastructure.database.session import get_db_session
from authx import AuthX
from passlib.context import CryptContext
import secrets

authx = AuthX()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(UserRepository(session), authx=authx, pwd_context=pwd_context)

def get_current_user(request: Request):  # Remove Depends()
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Access token not found in cookies")
    try:
        user = authx.decode_token(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid access token")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid access token: {str(e)}")

def get_refresh_token(request: Request):  # Remove Depends()
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token not found in cookies")
    try:
        payload = authx.decode_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid refresh token: {str(e)}")

def get_csrf_token():
    return secrets.token_hex(16)
