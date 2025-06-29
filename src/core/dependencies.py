from fastapi import Depends
from src.domain.services.user_service import UserService
from src.infrastructure.database.repositories.user_repository import SQLAlchemyUserRepository
from src.infrastructure.database.session import get_db_session

def get_user_service(session=Depends(get_db_session)) -> UserService:
    return UserService(SQLAlchemyUserRepository(session))
