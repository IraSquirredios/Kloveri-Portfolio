from pydantic import BaseModel


class Authentication_Schema(BaseModel):
    "Класс для аутентификации пользователя"
    username: str
    password: str