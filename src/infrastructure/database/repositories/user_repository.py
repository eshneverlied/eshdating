# from src.domain.entities.user import User
# from src.domain.repositories.user_repository import UserRepository
# from src.infrastructure.database.models.user import UserModel
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.future import select

# class SQLAlchemyUserRepository(UserRepository):
#     def __init__(self, session: AsyncSession):
#         self.session = session

#     async def create(self, user: User) -> User:
#         db_user = UserModel(email=user.email, password_hash=user.password_hash)
#         self.session.add(db_user)
#         await self.session.commit()
#         await self.session.refresh(db_user)
#         return User(id=db_user.id, email=db_user.email, password_hash=db_user.password_hash, created_at=db_user.created_at)

#     async def get_by_email(self, email: str) -> User | None:
#         result = await self.session.execute(select(UserModel).filter_by(email=email))
#         db_user = result.scalars().first()
#         return User(id=db_user.id, email=db_user.email, password_hash=db_user.password_hash, created_at=db_user.created_at) if db_user else None
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.domain.entities.user import User
from src.infrastructure.database.models.user import UserModel
from datetime import datetime

class SQLAlchemyUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).filter_by(email=email))
        user_model = result.scalars().first()
        if user_model:
            return User(
                id=user_model.id,
                email=user_model.email,
                password_hash=user_model.password_hash,
                created_at=user_model.created_at,
            )
        return None

    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(UserModel).filter_by(id=user_id))
        user_model = result.scalars().first()
        if user_model:
            return User(
                id=user_model.id,
                email=user_model.email,
                password_hash=user_model.password_hash,
                created_at=user_model.created_at,
            )
        return None

    async def create(self, user: User) -> User:
        """Создание пользователя из объекта User"""
        user_model = UserModel(
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)

        return User(
            id=user_model.id,
            email=user_model.email,
            password_hash=user_model.password_hash,
            created_at=user_model.created_at,
        )
