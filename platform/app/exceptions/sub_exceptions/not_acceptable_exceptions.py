from app.exceptions.main_exceptions import NotAcceptableException


class SerializationException(NotAcceptableException):
    def __init__(self):
        super().__init__(code="FAILED_SERIALIZATION", message="Ошибка сериализации")
