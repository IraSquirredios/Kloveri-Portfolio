"""
Декоратор для проверки прав доступа
"""
from functools import wraps
from typing import Optional, Union, Callable

from starlette.requests import Request
from token_sub_info.utils import get_token_from_request, validate_token

from app.config import settings
from app.exceptions.main_exceptions import ForbiddenException

from .schema import AuthConfig, AccessLevel, DebugMode
from .utils import get_user_auth_info, _has_permission, _is_access_denied, get_public_key


#   Выполняется только при старте приложения
def validate_permissions(permission_code: Union[str, Callable] = None):
    #   Если проверка отключена - возвращаем пустой декоратор
    if not settings.AUTH_ENABLED:
        def noop_decorator(func):
            return func
        return noop_decorator

    #   Обработка вызова без скобок: @validate_permissions
    if callable(permission_code):
        func = permission_code

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            return await _check_access(func, None, request, *args, **kwargs)
        return wrapper

    #   Обработка вызова с параметром: @validate_permissions("PERMISSION_CODE")
    def real_decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            return await _check_access(func, permission_code, request, *args, **kwargs)
        return wrapper

    return real_decorator


#   Проверка доступа в соответствии с настройками метода и правами пользователя
async def _check_access(func: Callable, permission_code: Optional[str], request: Request, *args, **kwargs):
    function_name = func.__name__
    auth_config: AuthConfig = request.app.state.auth_config

    #   Если не указан код права, считаем, что им является название функции
    if not permission_code:
        permission_code = function_name

    #   Получаем уровень доступа для функции
    access_level = auth_config.permissions.get(permission_code.lower())

    #   Проверяем доступ согласно логике DEV/PROD режимов
    if _is_access_denied(auth_config, access_level):
        raise ForbiddenException

    #   В dev-режиме отсутствие ограничений означает, что метод открыт
    if access_level is None and auth_config.debug_mode == DebugMode.DEV:
        access_level = AccessLevel.OPEN

    #   Получаем токен (может быть None для OPEN методов)
    if access_level != AccessLevel.OPEN:
        token = get_token_from_request(request)
        if not token:
            raise ForbiddenException

        #   Требуются конкретные права пользователя (явные или через группы)
        user_auth_info = get_user_auth_info(token)

        #   Пытаются использовать токен, выданный в другом продукте
        if user_auth_info.project_id and user_auth_info.project_id != request.headers.get('project-id'):
            raise ForbiddenException

    if access_level == AccessLevel.OPEN:
        #   Доступ открыт для всех - не требуется проверка
        pass

    elif access_level == AccessLevel.AUTHORIZED:
        #   Требуется только авторизация
        validate_token(token, get_public_key(), settings.JWT_ALGORITHM)

    elif access_level == AccessLevel.GRANTED:
        if not _has_permission(user_auth_info, permission_code, auth_config):
            raise ForbiddenException

    else:
        #   Пришло что-то непонятное. Вероятность нулевая (должно отвалиться на этапе чтения конфигов), но на всякий случай обработаем и ее
        print(f"Unknown level {access_level}")
        raise ForbiddenException

    #   Вызываем оригинальную функцию
    return await func(request, *args, **kwargs)
