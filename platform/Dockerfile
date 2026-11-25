# Versions
ARG PYTHON=python:3.12-alpine

## Stage one ##
FROM $PYTHON AS build
WORKDIR /usr/app
ARG BUILD_VERSION

# Установка uv (кэшируем отдельным слоем)
RUN pip install --no-cache-dir uv

# Создание venv через uv (без gcc и virtualenv)
ENV VIRTUAL_ENV="/usr/app/venv"
RUN uv venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Копируем и устанавливаем зависимости (кэшируемый слой)
COPY requirements.txt .
RUN uv pip install --no-cache -r requirements.txt

## Stage two ##
FROM $PYTHON AS runtime
ARG BUILD_VERSION

# Создание пользователя и директорий
RUN adduser -D cobra \
 && mkdir /usr/app \
 && chown cobra:cobra /usr/app
WORKDIR /usr/app

# Копируем только venv (без исходного кода пока)
COPY --chown=cobra:cobra --from=build /usr/app/venv ./venv

# Копируем только необходимый код (после venv для лучшего кэширования)
COPY --chown=cobra:cobra . .

# Settings
USER cobra
ENV VIRTUAL_ENV="/usr/app/venv"
ENV PATH="/usr/app/venv/bin:$PATH"
EXPOSE 80

# Переменные среды
ENV BUILD_VERSION=${BUILD_VERSION:-noversion}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Metadata
LABEL app.version="${BUILD_VERSION}"

# Запуск
ENTRYPOINT ["uvicorn", "application.main:app", "--host", "0.0.0.0"]
CMD ["--port", "80", "--proxy-headers"]
