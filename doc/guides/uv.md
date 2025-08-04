## ⚡ Что такое `uv`?

**`uv`** — это *сверхбыстрый* инструмент для управления зависимостями и виртуальными окружениями в Python:

* 🚀 **Очень быстрый** (написан на Rust)
* 🧱 **Поддерживает pyproject.toml**
* 🌀 Умеет **кешировать** зависимости и разрешения
* 🔒 Совместим с `pip`, `requirements.txt`, `poetry`, `pip-tools`

---

## 🛠️ Установка

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

или через `brew`:

```bash
brew install astral-sh/uv/uv
```

---

## 🚀 Основные команды

```bash
uv venv        # создаёт виртуальное окружение в .venv/
uv pip install <pkg>     # устанавливает пакет в окружение
uv pip freeze > req.txt  # сохраняет зависимости
uv pip sync req.txt      # синхронизирует окружение с requirements.txt

uv pip install -r requirements.txt  # установка из файла
```

Работает как `pip`, но **быстрее и безопаснее**.

---

## 🔧 Работа с `pyproject.toml`

`uv` поддерживает формат `PEP 621` — можно указывать зависимости в `pyproject.toml`:

```toml
[project]
name = "mybot"
dependencies = ["aiogram", "structlog", "python-dotenv"]

[build-system]
requires = ["uv"]
build-backend = "uv.pyproject.build"
```

Установка:

```bash
uv pip install -r <(uv pip compile pyproject.toml)
```

---

## 💡 Интеграция с проектом

Обновим предыдущие гайды с учётом `uv`.

---

## ✅ Обновлённый блок: Установка зависимостей (aiogram + structlog)

### Ранее:

```bash
pip install aiogram structlog
```

### Теперь с `uv`:

```bash
uv venv
uv pip install aiogram structlog python-dotenv
```

Чтобы зафиксировать зависимости:

```bash
uv pip freeze > requirements.txt
```

---

## ✅ Обновлённый блок: Структура проекта с `uv`

```
my-bot/
├── .venv/              # создаётся uv
├── bot.py
├── log.py
├── pyproject.toml      # опционально
├── requirements.txt
└── .env
```

> ❗ `.venv/` добавь в `.gitignore`

---

## ✅ Рекомендации по использованию

* Используй `uv venv` для локальных окружений
* Храни зависимости через `requirements.txt` или `pyproject.toml`
* Не смешивай `pip` и `uv` в одном проекте — выбирай одно
* Для CI/CD можно использовать `uv pip sync requirements.txt` — детерминировано и быстро

---

## 📚 Полезные ресурсы

* GitHub: [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
* Документация: [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
* PEP 621: [https://peps.python.org/pep-0621/](https://peps.python.org/pep-0621/)

---