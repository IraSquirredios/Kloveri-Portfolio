from pydantic import BaseModel, Field
from enum import StrEnum, IntEnum
from datetime import datetime, date

#   Поле типа "ключ - значение"
class FieldTitleValue(BaseModel):
    title: str
    value: str


#   Поле с описанием объекта
class FieldDescription(BaseModel):
    full: str | None = None
    preview: str | None = None


#   Поле с информацией об изображении объекта
class FieldImage(BaseModel):
    main: str | None = None
    preview: str | None = None
    cover: str | None = None
    icon: str | None = None
    emoji: str | None = None


#   Поле с описанием адреса (почтового, юридического и др.)
class FieldAddress(BaseModel):
    country: str | None = None
    region: str | None = None
    district: str | None = None
    settlement: str | None = None
    quarter: str | None = None
    street: str | None = None
    postcode: str | None = None
    house: str | None = None
    apartments: str | None = None
    room: str | None = None
    office: str | None = None
    entrance: str | None = None
    floor: str | None = None
    lat: str | None = None
    lon: str | None = None


#   Поле с описанием видеоконференции
class FieldVideoConference(BaseModel):
    platform: str | None = None         #   Система видеосвязи
    url: str | None = None              #   Адрес на трансляцию
    conference_id: str | None = None    #   ID трансляции в системе видеосвязи
    password: str | None = None         #   Код доступа к трансляции


#   Поле с типом действия
class FieldActionType(StrEnum):
    BUTTON = "button"
    LINK = "link"


#   Описание действия
class FieldAction(BaseModel):
    url: str
    title: str
    type: FieldActionType


#   Текст и описание
class FieldTitleDescriptionSimple(BaseModel):
    title: str | None = None
    description: str | None = None


#   Дата старта и окончания чего-либо
class FieldDates(BaseModel):
    start:  datetime | None = None
    finish: datetime | None = None


#   Подсказки для объектов
class FieldHint(BaseModel):
    text: str | None = None                 #   Текст подсказки
    url: str| None = None                   #   URL со справкой
    action_header: str | None = None        #   Заголовок кнопки или текст ссылки
    action: FieldActionType | None = None   #   Тип действия для получения подробной подсказки