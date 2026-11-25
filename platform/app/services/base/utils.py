import hashlib
from enum import IntEnum, StrEnum
from uuid import UUID

__version__ = "1.0.0"

#   Значения по умолчанию, когда сервис ожидает продукт, аккаунт или пользователя
DEFAULT_PROJECT = UUID("00000000-0000-0000-0000-000000000000")
DEFAULT_ACCOUNT = UUID("00000000-0000-0000-0000-000000000000")
DEFAULT_USER = UUID("00000000-0000-0000-0000-000000000000")


class Method(IntEnum):
    GET = 1
    POST = 2
    PUT = 3
    PATCH = 4
    DELETE = 5


class HeaderAlias(StrEnum):
    PROJECT_ID = "Project-ID"
    ACCOUNT_ID = "Account-ID"
    AUTHORIZATION = "Authorization"


class Timeout(IntEnum):
    FAST = 3
    MEDIUM = 10
    LONG = 60
    DEFAULT = 30


class Handle(StrEnum):
    PROFILES = "profiles"
    PRODUCTS = "account/my/products/"
    PRODUCT = "account/my/product/{product_id}/"
    DIRECTORY = "directory/{directory}"
    REPORTS_REPORT_ID = "reports/{report_id}"

    def resolve(self, **kwargs):
        return self.value.format(**kwargs)


def make_serialize_exception(method, schema, exception, data):
    print(f"Ошибка сериализации в методе {method}, схема {schema}.\n"
          f"Тип исключения: {type(exception).__name__}\nСообщение: {str(exception)}\n"
          f"Объект: {data}")


#   Склейка и сжатие уникального кода объекта или ссылки
def generate_object_code(*args):
    code_string = ''
    for _id in args:
        code_string += str(_id) + ":"
    code_string = code_string.rstrip(":")
    link_code_string_as_bytes = str.encode(code_string)
    hsh = hashlib.sha1()  # noqa: S324
    hsh.update(link_code_string_as_bytes)
    compressed_link_code = hsh.hexdigest()
    return compressed_link_code


#   Установка битового флага
def set_flag(flags: int, bit_pos: int) -> int:
    return flags | (1 << bit_pos)


#   Снятие битового флага
def clear_flag(flags: int, bit_pos: int) -> int:
    return flags & ~(1 << bit_pos)


#   Проверка битового флага
def test_flag(flags: int, bit_pos: int) -> bool:
    return bool(flags & (1 << bit_pos))


#   Проверка, что значение является UUID
def is_uuid(id_) -> bool:
    try:
        UUID(id_)
        return True
    except ValueError:
        return False


#   Находит массив общих ключей для двух словарей
def find_common_keys(dict1, dict2):
    common_keys = set(dict1.keys()) & set(dict2.keys())
    return list(common_keys)


#   Проверка, что класс содержит указанный атрибут
def check_attribute(obj, attr_name):
    return 1 if attr_name in obj.__members__.values() else 0


# Универсальная функция для извлечения атрибута из структуры
#    Извлекает атрибут объекта, проверяя сначала наличие ключа в словаре,
#    затем используя getattr() для объектов классов.
def extract_attribute(obj, attr_name):
    # Проверяем, является ли объект словарем и содержит ли нужный ключ
    if isinstance(obj, dict) and obj.get(attr_name):
        return obj[attr_name]

    # Если объект не словарь, пытаемся получить атрибут методом getattr()
    try:
        return getattr(obj, attr_name)
    except AttributeError:
        return None


#   Возвращет значение аккаунта по умолчанию, если не передан извне
def get_account(account_id):
    _account_id = _check_uuid(account_id)
    return _account_id if _account_id is not None else DEFAULT_ACCOUNT


#   Возвращает значение пользователя по умолчанию, если не передан извне
def get_user(user_id):
    _user_id = _check_uuid(user_id)
    return _user_id if _user_id is not None else DEFAULT_USER


#   Возвращает значение продукта по умолчанию, если не передан извне
def get_project(project_id):
    _project_id = _check_uuid(project_id)
    return _project_id if _project_id is not None else DEFAULT_PROJECT


def _check_uuid(param):
    # Если в переменной строка, преобразуем её в UUID
    if isinstance(param, str):
        return UUID(param)

    # Если в переменной уже объект UUID, возвращаем его
    if isinstance(param, UUID):
        return param

    return param
