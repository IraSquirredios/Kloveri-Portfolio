"""
Основные классы и схемы для системы аутентификации
"""
from enum import StrEnum
from typing import Dict, Set, Optional
from pydantic import BaseModel


class DebugMode(StrEnum):
    PROD = "PROD"
    DEV = "DEV"


class AccessLevel(StrEnum):
    GRANTED = "GRANTED"
    OPEN = "OPEN"
    AUTHORIZED = "AUTHORIZED"
    BLOCKED = "BLOCKED"


class AuthConfig(BaseModel):
    debug_mode: DebugMode
    permissions: Dict[str, AccessLevel] = {}    # function_name -> AccessLevel
    groups: Dict[str, Set[str]] = {}            # group_name -> set of function_names


#   Информация о правах пользователя
class UserAuthInfo(BaseModel):
    user_permissions: Set[str]  # Явно указанные права пользователя в токене
    groups: Set[str]            # Группы пользователя
    all_permissions: Set[str]   # Все права (явные + групповые)
    project_id: str             # ID проекта, в котором выданы права
