from datetime import datetime

from pyrogram import Client

from src.core.config import settings
from src.domain.entities.telegram_session import TelegramSession


class TelegramSessionService:
    def __init__(self, repository):
        self.repo = repository
        # Temporary store for ongoing authorizations
        self._pending: dict[str, dict] = {}

    async def add_session(
        self,
        user_id: int,
        session_name: str,
        api_id: int,
        api_hash: str,
    ) -> None:
        """Start session creation by storing initial parameters."""

        self._pending[session_name] = {
            "user_id": user_id,
            "api_id": api_id,
            "api_hash": api_hash,
        }

    async def provide_phone(self, session_name: str, phone: str) -> None:
        """Send authentication code to the given phone number."""

        data = self._pending.get(session_name)
        if not data:
            raise ValueError("Session not initialized")

        client = Client(
            session_name,
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            workdir=settings.TG_SESSION_DIR,
        )

        await client.connect()
        sent_code = await client.send_code(phone)
        await client.disconnect()

        data["phone"] = phone
        data["phone_code_hash"] = sent_code.phone_code_hash

    async def confirm_code(
        self,
        session_name: str,
        code: str,
        password: str | None = None,
    ) -> TelegramSession:
        """Finalize authorization with the received code and optional password."""

        data = self._pending.get(session_name)
        if not data:
            raise ValueError("Session not initialized")

        client = Client(
            session_name,
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            workdir=settings.TG_SESSION_DIR,
        )

        await client.connect()
        await client.sign_in(
            phone_number=data["phone"],
            phone_code_hash=data["phone_code_hash"],
            phone_code=code,
            password=password,
        )
        await client.disconnect()

        session = TelegramSession(
            id=0,
            user_id=data["user_id"],
            session_name=session_name,
            api_id=data["api_id"],
            api_hash=data["api_hash"],
            created_at=datetime.utcnow(),
        )

        result = await self.repo.create(session)
        self._pending.pop(session_name, None)
        return result

