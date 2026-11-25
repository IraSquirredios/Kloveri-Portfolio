"""
Вспомогательные функции для системы аутентификации
"""
from typing import Dict, Set, Optional
from token_sub_info.get_info import get_all_info
from token_sub_info.utils import get_token_from_request

from app.config import settings

from .schema import AuthConfig, UserAuthInfo, AccessLevel, DebugMode

#   Получение публичного ключа в формате, в которым мы храним подобные ключи
def get_public_key() -> bytes:
    return settings.ACCESS_TOKEN_PUBLIC_KEY.replace("\\n", "\n").encode()


#   Проверяет, запрещен ли доступ согласно общим правилам окружений
def _is_access_denied(auth_config: AuthConfig, access_level: Optional[AccessLevel]) -> bool:
    # Случай 1: Метод явно заблокирован
    if access_level == AccessLevel.BLOCKED:
        return True

    # Случай 2: В конфигурации включен PROD-режим и метод не сконфигурирован - блокируем доступ
    if auth_config.debug_mode == DebugMode.PROD and access_level is None:
        return True

    # Остальные варианты проверим далее, в т.ч. случай 3: Включен DEV-режим и метод не сконфигурирован - разрешаем доступ
    return False


#   Получает полную информацию о правах пользователя
def get_user_auth_info(token: str) -> UserAuthInfo:
    #   Получаем полные данные из токена, чтобы не делать многократно
    user_data = get_all_info(token, get_public_key(), settings.JWT_ALGORITHM)

    # Получаем явные права пользователя
    user_permissions = get_user_permissions(user_data)

    # Получаем группы пользователя
    user_groups = get_user_groups(user_data)

    # Собираем все права пользователя (явные + групповые)
    # Групповые пока ставим как копию пользовательских
    all_permissions = user_permissions.copy()


    # Обязательно вернем продукт, в котором выдан токен
    user_product = get_user_project(user_data)

    return UserAuthInfo(
        user_permissions=user_permissions,
        groups=user_groups,
        all_permissions=all_permissions,
        project_id=user_product
    )


#   Права пользователя в данном сервисе
def get_user_permissions(token_data: dict):
    user_permissions = token_data.get("permissions")
    explicit_permissions = get_service_data(user_permissions)
    return explicit_permissions


#   Группы доступа в сервисе
def get_user_groups(token_data: dict):
    groups = token_data.get("groups")
    explicit_groups = get_service_data(groups)
    return explicit_groups


#   Продукт, в котором есть права
def get_user_project(token_data: dict):
    return token_data.get("project_id")


#   Службная функция для перевода прав/групп в формат множества
def get_service_data(all_data):
    explicit_data = set()
    if all_data and settings.SERVICE_NAME in all_data:
        service_data = all_data[settings.SERVICE_NAME]
        if isinstance(service_data, list):
            explicit_data = set(service_data)
        elif isinstance(service_data, dict):
            explicit_data = set(service_data.keys())

    return explicit_data


#   Получение всех прав пользователя в данном сервисе
def get_all_permissions(auth_config: AuthConfig, user_auth_info: UserAuthInfo) -> UserAuthInfo:
    _permissions = set(user_auth_info.user_permissions)
    for group_name in user_auth_info.groups:
        _permissions = _permissions.union(set(auth_config.groups[group_name]))

    return UserAuthInfo(
        user_permissions=user_auth_info.user_permissions,
        groups=user_auth_info.groups,
        all_permissions=_permissions
    )


#   Персональные и групповые права в сервисе
def get_user_service_info(request) -> UserAuthInfo:
    # Нужен конфиг с настройками прав и групп
    auth_config: AuthConfig = request.app.state.auth_config

    token = get_token_from_request(request)
    user_auth_info = get_user_auth_info(token)
    return get_all_permissions(auth_config, user_auth_info)


#   Проверяет, есть ли у пользователя право на выполнение функции
def _has_permission(user_auth_info: UserAuthInfo, permission_name: str, auth_config: AuthConfig) -> bool:
    if not permission_name:
        return False

    method_code = permission_name.lower()

    # ПРИОРИТЕТ 1: Проверяем явные права пользователя
    if method_code in user_auth_info.user_permissions:
        return True

    # ПРИОРИТЕТ 2: Проверяем права через группы
    for group_name in user_auth_info.groups:
        if group_name in auth_config.groups and method_code in auth_config.groups[group_name]:
            return True

    return False


#   Возвращает информацию о текущей конфигурации прав
def get_lib_info(auth_config: AuthConfig) -> dict:
    result = {
        "auth_enabled": settings.AUTH_ENABLED,
        "debug_mode": auth_config.debug_mode.value,
        "environment": settings.ENVIRONMENT,
        "permissions": {
            function_name: level.value
            for function_name, level in auth_config.permissions.items()
        },
        "groups": {
            group_name: list(function_names)
            for group_name, function_names in auth_config.groups.items()
        }
    }
    return result


#   Возвращает уровень доступа для функции (для отладки)
def get_function_access_level(auth_config: AuthConfig, function_name: str) -> str:
    access_level = auth_config.permissions.get(function_name)

    if access_level:
        return access_level.value
    elif auth_config.debug_mode == DebugMode.DEV:
        return "OPEN (DEV mode default)"
    else:
        return "DENIED (PROD mode default)"
