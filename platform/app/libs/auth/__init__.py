"""
Библиотека аутентификации в Цербере.
Публичный интерфейс
"""

__version__ = "1.2.0"
__name__ = "auth"

from app.config import settings

from .config_loader import _init_auth
from .schema import DebugMode, AccessLevel, AuthConfig, UserAuthInfo

if settings.AUTH_ENABLED:
    # Реальные импорты когда модуль включен
    from .decorators import validate_permissions
    from .config_loader import parse_auth, validate_auth_config_on_startup
    from .utils import get_lib_info, get_function_access_level
else:
    # Заглушки когда модуль отключен
    from .stubs import (
        validate_permissions,
        parse_auth,
        get_lib_info,
        get_function_access_level,
        validate_auth_config_on_startup
    )


#   Инициализация аутентификации в приложении
def init_auth(app):
    if settings.AUTH_ENABLED:
        _init_auth(app)


__all__ = [
    'validate_permissions',
    'parse_auth',
    'get_lib_info',
    'get_function_access_level',
    'init_auth',
    'DebugMode',
    'AccessLevel',
    'AuthConfig',
    'UserAuthInfo',
    'validate_auth_config_on_startup'
]