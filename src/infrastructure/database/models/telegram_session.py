from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from .user import Base

class TelegramSessionModel(Base):
    __tablename__ = "telegram_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_name = Column(String, unique=True, nullable=False)
    api_id = Column(Integer, nullable=False)
    api_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
