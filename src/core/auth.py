from authx import AuthX, AuthXConfig  # убедитесь, что импортируете AuthXConfig
from src.core.config import settings

# Конфигурация AuthX – указываем использование cookies для токенов
authx_config = AuthXConfig(
    JWT_SECRET_KEY=settings.JWT_SECRET_KEY,
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_TOKEN_EXPIRES=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    JWT_REFRESH_TOKEN_EXPIRES=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    JWT_TOKEN_LOCATION=["cookies"],            # Разрешаем искать JWT в cookies
    JWT_ACCESS_COOKIE_NAME="access_token",     # Имя cookie для access-токена
    JWT_REFRESH_COOKIE_NAME="refresh_token",   # Имя cookie для refresh-токена
    JWT_COOKIE_CSRF_PROTECT=False,             # Отключаем требование CSRF-токена для упрощения
    JWT_COOKIE_SECURE=False,                  # Secure=False, т.к. используем http на локалхосте
    JWT_COOKIE_SAMESITE="lax"                  # Политика SameSite для cookies
)

# Создание экземпляра AuthX
authx = AuthX(config=authx_config)

# Функция-помощник для получения экземпляра AuthX (если требуется где-либо)
def get_authx():
    """Возвращает экземпляр AuthX"""
    return authx
