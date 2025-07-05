from pydantic import BaseModel, Field
from typing import Optional

class TelegramSessionCreate(BaseModel):
    session_name: str
    api_id: int
    api_hash: str
    phone: str
    otp: str = Field(..., description="One-time code sent to Telegram")
    password: Optional[str] = None
