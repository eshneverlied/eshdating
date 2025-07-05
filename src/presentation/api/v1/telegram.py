from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import (
    get_current_user,
    get_telegram_session_service,
)
from src.domain.services.telegram_session_service import TelegramSessionService
from src.presentation.schemas.telegram_session import TelegramSessionCreate

router = APIRouter(prefix="/api/v1/telegram", tags=["telegram"])


@router.post("/telegram/sessions")
async def create_telegram_session(
    session_data: TelegramSessionCreate,
    current_user=Depends(get_current_user),
    service: TelegramSessionService = Depends(get_telegram_session_service),
):
    """Create and store a new Telegram session."""
    try:
        session = await service.add_session(
            user_id=current_user["id"],
            session_name=session_data.session_name,
            api_id=session_data.api_id,
            api_hash=session_data.api_hash,
            phone=session_data.phone,
            code=session_data.otp,
            password=session_data.password,
        )
        return {
            "id": session.id,
            "session_name": session.session_name,
            "api_id": session.api_id,
            "api_hash": session.api_hash,
            "created_at": session.created_at,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
