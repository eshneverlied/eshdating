from dataclasses import dataclass
from datetime import datetime


@dataclass
class TelegramSession:
    id: int
    user_id: int
    session_name: str
    api_id: int
    api_hash: str
    created_at: datetime
