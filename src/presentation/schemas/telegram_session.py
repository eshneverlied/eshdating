from pydantic import BaseModel, Field
from typing import Optional


class TelegramSessionStart(BaseModel):
    session_name: str
    api_id: int
    api_hash: str


class TelegramSessionPhone(BaseModel):
    session_name: str
    phone: str


class TelegramSessionConfirm(BaseModel):
    session_name: str
    otp: str = Field(..., description="One-time code sent to Telegram")
    password: Optional[str] = None
