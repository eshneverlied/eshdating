from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.user import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        db_user = UserModel(email=user.email, password_hash=user.password_hash)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return User(id=db_user.id, email=db_user.email, password_hash=db_user.password_hash, created_at=db_user.created_at)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(UserModel).filter_by(email=email))
        db_user = result.scalars().first()
        return User(id=db_user.id, email=db_user.email, password_hash=db_user.password_hash, created_at=db_user.created_at) if db_user else None
