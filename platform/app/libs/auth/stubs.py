"""
Заглушки для отключенного режима аутентификации
"""
from enum import StrEnum
from typing import Dict, Set, Optional, Any
from pydantic import BaseModel
from fastapi import FastAPI

from .schema import AuthConfig, DebugMode, UserAuthInfo

#   Пустой декоратор - пропускает все запросы
def validate_permissions(permission_code: str = None):
    def decorator(func):
        return func
    return decorator


#   Заглушка парсера конфигурации
def parse_auth() -> AuthConfig:
    return AuthConfig(debug_mode=DebugMode.DEV)


#   Заглушка валидации конфига
def validate_auth_config_on_startup(auth_config: AuthConfig):
    print("🔓 Authentication disabled - all access granted")


#   Информация о заглушке аутентификации
def get_lib_info(auth_config: AuthConfig) -> dict:
    return {
        "auth_enabled": False,
        "message": "Authentication system is disabled"
    }


#   Уровень доступа для функции в отключенном режиме
def get_function_access_level(auth_config: AuthConfig, function_name: str) -> str:
    return "OPEN (auth disabled)"


#   Заглушка инициализации
def init_auth(app: FastAPI):
    app.state.auth_config = AuthConfig()
    print("🔓 Authentication system disabled - all access granted")
