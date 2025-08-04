Вот краткий, но содержательный гайд по **`structlog`** — библиотеке для **структурированного логирования** в Python.

---

## 🔧 Что такое `structlog`?

`structlog` — это обёртка над стандартным модулем `logging`, позволяющая:

* логировать в **структурированном виде** (dict, JSON)
* легко добавлять **контекст** (например, user\_id, request\_id)
* удобно фильтровать и анализировать логи (в консоли или в системах мониторинга)

---

## 🚀 Установка

```bash
uv venv
uv pip install aiogram structlog python-dotenv
```

Чтобы зафиксировать зависимости:

```bash
uv pip freeze > requirements.txt
```


Если нужны JSON-логи:

```bash
pip install structlog[json]
```

---

## 🔨 Базовая настройка

```python
import logging
import structlog

logging.basicConfig(level=logging.INFO, format="%(message)s")

structlog.configure(
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),  # для dev-режима
    ]
)

log = structlog.get_logger()

log.info("App started", version="1.0", mode="dev")
```

---

## 🧩 Логгирование с контекстом

```python
log = structlog.get_logger().bind(user_id=123, session="abc")

log.info("User logged in", action="login")
log.warning("Suspicious activity", ip="10.0.0.1")
```

Результат (в dev-режиме):

```
2025-08-04T10:00:00Z [info     ] User logged in     [user_id=123 session=abc action=login]
```

---

## 🛠 Пример с JSON-логами

```python
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ]
)

log = structlog.get_logger()
log.info("Processed payment", user_id=42, amount=100)
```

Вывод:

```json
{
  "event": "Processed payment",
  "timestamp": "2025-08-04T10:00:00Z",
  "level": "info",
  "user_id": 42,
  "amount": 100
}
```

---

## 📦 Практика: интеграция с приложением

```python
# log.py
import logging
import structlog

def setup_logging():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.dev.ConsoleRenderer()
        ]
    )
```

```python
# main.py
from log import setup_logging
import structlog

setup_logging()
log = structlog.get_logger().bind(service="telegram_bot")

log.info("Bot started")
log.warning("Message parse failed", raw_text="???", user_id=321)
```

---

## 🎯 Рекомендации

* Используй `.bind(...)` для добавления контекста (user\_id, task\_id и т.п.)
* Для продакшена — `JSONRenderer`, для локальной отладки — `ConsoleRenderer`
* Работает прекрасно с `uvicorn`, `fastapi`, `aiogram`, `click` и пр.
* Удобно интегрируется с лог-агрегаторами (ELK, Grafana Loki, Sentry)

---

## 📚 Полезные ресурсы

* Документация: [https://www.structlog.org/en/stable/](https://www.structlog.org/en/stable/)
* Пример с FastAPI: [https://fastapi.tiangolo.com/advanced/logging/](https://fastapi.tiangolo.com/advanced/logging/)
* GitHub: [https://github.com/hynek/structlog](https://github.com/hynek/structlog)

---