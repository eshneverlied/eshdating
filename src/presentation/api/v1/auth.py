from fastapi import APIRouter, HTTPException, Depends,status
from src.domain.services.user_service import UserService
from src.presentation.schemas.user import UserCreate, User, UserLogin, Token
from src.core.dependencies import get_user_service
from fastapi.responses import JSONResponse
router = APIRouter()

@router.post("/register", response_model=User)
async def register_user(user_data: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        user = await user_service.register(user_data.email, user_data.password)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=Token)
async def login_user(user_data: UserLogin, user_service: UserService = Depends(get_user_service)):
    try:
        token = await user_service.login(user_data.email, user_data.password)
        return token
    except HTTPException as e:
        raise e

@router.post("/logout", status_code=200, tags=["Auth"])
async def logout_user():
    """
    Информирует клиент, что токен нужно удалить
    !!!ПЕРЕДЕЛАТЬ С REDIS!!!
    """
    return JSONResponse(
        content={"message": "Successfully logged out. Please delete your token on the client side."},
        status_code=status.HTTP_200_OK
    )
