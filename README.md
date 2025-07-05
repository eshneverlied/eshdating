# Dating Portal

A scalable backend for a dating platform using FastAPI, PostgreSQL, and AuthX.

## Setup

1. Install `uv`: `pip install uv`
2. Create virtual environment: `uv init --python 3.11`
3. Install dependencies: `uv sync`
4. Copy `.env.example` to `.env` and configure. Ensure `TG_SESSION_DIR` points to
   the directory where Telegram session files should be stored.
5. Run migrations: `alembic upgrade head`
6. Start server: `uvicorn src.main:app --reload`

## Endpoints

- POST `/api/v1/auth/register`: Register a new user.
- POST `/api/v1/auth/login`: Login and get JWT token.
- POST `/api/v1/telegram/sessions/start`: Begin creating a Telegram session
- POST `/api/v1/telegram/sessions/phone`: Provide phone number and request OTP
- POST `/api/v1/telegram/sessions/confirm`: Submit OTP and optional password
- GET `/telegram/add`: Web form for Telegram session setup
