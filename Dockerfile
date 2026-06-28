FROM python:3.12.3-slim

# Создаем пользователя celery
RUN adduser --system --group --no-create-home celery

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_VIRTUALENVS_IN_PROJECT=false
ENV PYTHONUNBUFFERED=1

WORKDIR /apps

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY README.md /apps/README.md
COPY pyproject.toml poetry.lock ./
COPY . .

# Установка зависимостей через pip из poetry.lock
RUN pip install toml-to-requirements && \
    toml-to-req --toml-file pyproject.toml && \
    pip install -r requirements.txt && \
    pip install poetry==2.2.1

# Меняем владельца файлов
RUN chown -R celery:celery /apps && \
    chmod +x manage.py

USER celery

EXPOSE 8000