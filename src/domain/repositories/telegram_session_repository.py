from abc import ABC, abstractmethod
from typing import Iterable, Optional

from src.domain.entities.telegram_session import TelegramSession


class TelegramSessionRepository(ABC):
    @abstractmethod
    async def create(self, session: TelegramSession) -> TelegramSession:
        """Persist a Telegram session."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_user(self, user_id: int) -> Iterable[TelegramSession]:
        """Return all sessions belonging to a user."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, session_id: int) -> Optional[TelegramSession]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_session_name(self, session_name: str) -> Optional[TelegramSession]:
        raise NotImplementedError
