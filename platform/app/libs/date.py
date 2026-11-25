from enum import StrEnum, IntEnum
from datetime import datetime, timedelta, timezone
from pydantic import BeforeValidator
from typing_extensions import Annotated
from pydantic_core import core_schema

__version__ = "1.1.0"

#   Основной класс настроек дат
class DateSettings:
    #   Строковые значения формата даты-времени
    class Format(StrEnum):
        DATE    = "%Y-%m-%d"
        DEFAULT = "%Y-%m-%d %H:%M:%S %z"

    #   Целочисленные настройки (например, часовой пояс)
    class Timezone(IntEnum):
        DEFAULT = 3  # UTC+3 (Москва)


#   Преобразование даты из Unix-time в обычное представление
def make_date(unix_timestamp, format = None, tzone = None):
    f = format if format else DateSettings.Format.DEFAULT

    # Преобразуем timestamp в объект datetime
    dt = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)

    # Преобразуем в нужную временную зону. По умолчанию - часовой пояс мск
    tz = DateSettings.Timezone.DEFAULT if not tzone else int(tzone)
    target_tz = timezone(timedelta(hours=tz))
    converted_dt = dt.astimezone(target_tz)

    # Форматируем дату в нужный формат
    return converted_dt.strftime(f)


# Преобразует входное значение в ISO-строку datetime с timezone.
# Входные параметры:
#   value: datetime | str | None - значение для преобразования
# Выходные параметры:
#   str | None - ISO-строка datetime с timezone или None
def parse_datetime(value: datetime | str | None) -> str | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        # Приводим к UTC и возвращаем ISO-строку
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, str):
        try:
            # Парсим строку в datetime и приводим к UTC
            dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
            return dt.astimezone(timezone.utc).isoformat()
        except ValueError:
            return None
    return None


#   Обработчик для парсинга строки datetime с временной зоной
def parse_datetime_with_timezone(value) -> datetime:
    if isinstance(value, str):
        # Парсим из строки нашего формата
        return datetime.strptime(value, DateSettings.Format.DEFAULT)
    elif isinstance(value, (int, float)):
        # Парсим из timestamp
        return datetime.fromtimestamp(value, tz=timezone.utc)
    elif isinstance(value, datetime):
        # Уже datetime объект
        return value
    else:
        raise ValueError(f"Unsupported type for datetime parsing: {type(value)}")


#   Функция для сериализации datetime в нужный формат
def serialize_datetime(dt: datetime) -> str:
    return dt.strftime(DateSettings.Format.DEFAULT)


#   Ищем дату полночи дня на days больше/меньше указанного
#       реестры пока не умеют в поиск точного времени
def get_midnight(date_str, days):
    #   Добавляем нужное число дней
    day_delta = date_str + timedelta(days=days)

    #   Устанавливаем время ровно на полночь
    midnight = day_delta.replace(hour=0, minute=0, second=0, microsecond=0)

    return midnight.strftime("%Y-%m-%d %H:%M:%S")


# Функция для сравнения полной временной отметки (дата+время)
def compare_datetimes(dt1, dt2):
    result = 0
    if isinstance(dt1, str):
        dt1 = datetime.fromisoformat(dt1)  # Парсим ISO-временную отметку
    if isinstance(dt2, str):
        dt2 = datetime.fromisoformat(dt2)  # То же самое для второго аргумента

    # Приводим оба объекта к UTC
    dt1_utc = dt1.astimezone(timezone.utc)
    dt2_utc = dt2.astimezone(timezone.utc)

    if dt1_utc < dt2_utc:
        result = -1
    elif dt1_utc > dt2_utc:
        result = 1
    return result


# Кастомный тип даты и времени с правильной валидацией и сериализацией
class DatetimeWithTimezoneType:
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type, _handler):

        def validate_value(value: any, handler: core_schema.ValidatorFunctionWrapHandler) -> datetime:
            # Если значение уже datetime, пропускаем как есть
            if isinstance(value, datetime):
                return value
            # Если строка или число - парсим нашим методом
            return parse_datetime_with_timezone(value)

        def serialize_value(value: datetime) -> str:
            return serialize_datetime(value)

        return core_schema.general_after_validator_function(
            validate_value,
            core_schema.union_schema([
                core_schema.datetime_schema(),
                core_schema.str_schema(),
                core_schema.int_schema(),
                core_schema.float_schema()
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                serialize_value,
                info_arg=False,
                return_schema=core_schema.str_schema()
            )
        )


DatetimeWithTimezone = Annotated[
    datetime,
    DatetimeWithTimezoneType
]
