"""
    Работа с токеном авторизации
"""
from typing import Dict, Set, Optional

from token_sub_info.get_info import get_all_info
from token_sub_info.utils import get_token_from_request, validate_token

from app.config import settings
from app.schemas.base.token_schemas import TokenInfo

#   Получает информацию о содержимом токена
def token_info(request, key: bytes = None, jwt: str = None):
    token = get_token_from_request(request=request)
    #   Проверим, что токен валидный для данного ключа и алгоритма
    validate_token(token, __get_key(key), __get_jwt(jwt))
    return token_get(token, key, jwt)


#   Получает содержимое токена
def token_get(token: str, key: bytes = None, jwt: str = None):
    token_data = get_all_info(token, __get_key(key), __get_jwt(jwt))
    return TokenInfo(
        project_id      = token_get_project(token_data),
        account_id      = token_get_account(token_data),
        user_id         = token_get_user(token_data),
        profile_id      = token_get_profile(token_data),
        device_id       = token_get_device(token_data),
        organizations   = token_get_orgs(token_data),
        permissions     = token_get_permissions(token_data),
        groups          = token_get_groups(token_data),
    )


#   Права пользователя в данном сервисе
def token_get_permissions(token_data: dict):
    user_permissions = token_data.get("permissions")
    explicit_permissions = __get_service_data(user_permissions)
    return explicit_permissions

#   Группы доступа в сервисе
def token_get_groups(token_data: dict):
    groups = token_data.get("groups")
    explicit_groups = __get_service_data(groups)
    return explicit_groups

#   Продукт, в котором есть права
def token_get_project(token_data: dict):
    return token_data.get("project_id")

#   Аккаунт
def token_get_account(token_data: dict):
    return token_data.get("account_id")

#   Пользователь
def token_get_user(token_data: dict):
    return token_data.get("user_id")

#   Профиль
def token_get_profile(token_data: dict):
    return token_data.get("profile_id")

#   Устройство
def token_get_device(token_data: dict):
    return token_data.get("device_id")

#   Организации
def token_get_orgs(token_data: dict):
    return token_data.get("organizations")



#   СЛУЖЕБНЫЕ ФУНКЦИИ

#   Получение публичного ключа в формате, в которым мы храним подобные ключи
def __get_key(key) -> bytes:
    _token = key if key is not None else settings.ACCESS_TOKEN_PUBLIC_KEY
    return _token.replace("\\n", "\n").encode()


#   Получение алгоритма для расшифровки токена
def __get_jwt(algorithm) -> str:
    return algorithm if algorithm is not None else settings.JWT_ALGORITHM

#   Службная функция для перевода прав/групп в формат множества
def __get_service_data(all_data):
    explicit_data = set()
    if all_data and settings.SERVICE_NAME in all_data:
        service_data = all_data[settings.SERVICE_NAME]
        if isinstance(service_data, list):
            explicit_data = set(service_data)
        elif isinstance(service_data, dict):
            explicit_data = set(service_data.keys())

    return explicit_data
