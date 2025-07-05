from datetime import datetime

from pyrogram import Client

from src.core.config import settings
from src.domain.entities.telegram_session import TelegramSession


class TelegramSessionService:
    def __init__(self, repository):
        self.repo = repository

    async def add_session(
        self,
        user_id: int,
        session_name: str,
        api_id: int,
        api_hash: str,
        phone: str,
        code: str,
        password: str | None = None,
    ) -> TelegramSession:
        """Create a Telegram session file and persist its metadata."""

        client = Client(
            session_name,
            api_id=api_id,
            api_hash=api_hash,
            workdir=settings.TG_SESSION_DIR,
        )

        await client.connect()
        await client.send_code(phone)
        await client.sign_in(phone, code, password=password)
        await client.disconnect()

        session = TelegramSession(
            id=0,
            user_id=user_id,
            session_name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            created_at=datetime.utcnow(),
        )

        return await self.repo.create(session)

