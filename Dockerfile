FROM python:3.13-slim

WORKDIR /app

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Установка uv
RUN pip install --no-cache-dir uv

# Копирование файлов конфигурации
COPY pyproject.toml uv.lock* ./

# Установка зависимостей
RUN uv pip install . --system --no-cache

# Копирование исходного кода
COPY . .

# Создание непривилегированного пользователя
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

CMD ["python", "main.py"]