from fastapi import APIRouter, Depends, HTTPException

from src.core.dependencies import (
    get_current_user,
    get_telegram_session_service,
)
from src.domain.services.telegram_session_service import TelegramSessionService
from src.presentation.schemas.telegram_session import (
    TelegramSessionStart,
    TelegramSessionPhone,
    TelegramSessionConfirm,
)

router = APIRouter(prefix="/api/v1/telegram", tags=["telegram"])


@router.post("/telegram/sessions/start")
async def start_session(
    data: TelegramSessionStart,
    current_user=Depends(get_current_user),
    service: TelegramSessionService = Depends(get_telegram_session_service),
):
    """Initialize session creation and request phone."""
    try:
        await service.add_session(
            user_id=current_user["id"],
            session_name=data.session_name,
            api_id=data.api_id,
            api_hash=data.api_hash,
        )
        return {"detail": "phone required"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/telegram/sessions/phone")
async def send_phone(
    data: TelegramSessionPhone,
    current_user=Depends(get_current_user),
    service: TelegramSessionService = Depends(get_telegram_session_service),
):
    """Send phone number and request OTP."""
    try:
        await service.provide_phone(data.session_name, data.phone)
        return {"detail": "otp required"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/telegram/sessions/confirm")
async def confirm_code(
    data: TelegramSessionConfirm,
    current_user=Depends(get_current_user),
    service: TelegramSessionService = Depends(get_telegram_session_service),
):
    """Finalize authorization with OTP and optional password."""
    try:
        session = await service.confirm_code(
            session_name=data.session_name,
            code=data.otp,
            password=data.password,
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
