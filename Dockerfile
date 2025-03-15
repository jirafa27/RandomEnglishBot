# Используем базовый образ Python 3.9-slim
FROM python:3.9-slim

# Устанавливаем переменные окружения для неинтерактивной установки пакетов и подавления ошибок narrowing
ENV DEBIAN_FRONTEND=noninteractive
ENV CFLAGS="-Wno-narrowing"
ENV PYTHONPATH="/app"

# Обновляем списки пакетов и устанавливаем необходимые системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей и устанавливаем Python-пакеты
COPY requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt


COPY . /app/

# Указываем команду запуска приложения/бота
CMD ["python", "-m", "bot.main"]
