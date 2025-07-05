from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.domain.entities.telegram_session import TelegramSession
from src.domain.repositories.telegram_session_repository import TelegramSessionRepository
from src.infrastructure.database.models.telegram_session import TelegramSessionModel


class SQLAlchemyTelegramSessionRepository(TelegramSessionRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, session_obj: TelegramSession) -> TelegramSession:
        db_model = TelegramSessionModel(
            user_id=session_obj.user_id,
            session_name=session_obj.session_name,
            api_id=session_obj.api_id,
            api_hash=session_obj.api_hash,
            created_at=session_obj.created_at,
        )
        self.session.add(db_model)
        await self.session.commit()
        await self.session.refresh(db_model)
        return TelegramSession(
            id=db_model.id,
            user_id=db_model.user_id,
            session_name=db_model.session_name,
            api_id=db_model.api_id,
            api_hash=db_model.api_hash,
            created_at=db_model.created_at,
        )

    async def get_by_user(self, user_id: int) -> list[TelegramSession]:
        result = await self.session.execute(
            select(TelegramSessionModel).filter_by(user_id=user_id)
        )
        models = result.scalars().all()
        return [
            TelegramSession(
                id=m.id,
                user_id=m.user_id,
                session_name=m.session_name,
                api_id=m.api_id,
                api_hash=m.api_hash,
                created_at=m.created_at,
            )
            for m in models
        ]

    async def get_by_id(self, session_id: int) -> TelegramSession | None:
        result = await self.session.execute(
            select(TelegramSessionModel).filter_by(id=session_id)
        )
        model = result.scalars().first()
        if model:
            return TelegramSession(
                id=model.id,
                user_id=model.user_id,
                session_name=model.session_name,
                api_id=model.api_id,
                api_hash=model.api_hash,
                created_at=model.created_at,
            )
        return None

    async def get_by_session_name(self, session_name: str) -> TelegramSession | None:
        result = await self.session.execute(
            select(TelegramSessionModel).filter_by(session_name=session_name)
        )
        model = result.scalars().first()
        if model:
            return TelegramSession(
                id=model.id,
                user_id=model.user_id,
                session_name=model.session_name,
                api_id=model.api_id,
                api_hash=model.api_hash,
                created_at=model.created_at,
            )
        return None
