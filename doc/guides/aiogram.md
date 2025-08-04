## 🚀 Установка

```bash
uv pip install -U aiogram
```

---

## 🧠 Архитектура

`aiogram` использует **асинхронный диспетчер событий** и построен вокруг:

* `Bot` — клиент Telegram API
* `Dispatcher` — маршрутизатор обновлений
* `Router` — группирует хендлеры
* `FSM` — конечные автоматы состояний (для диалогов)
* `Middleware` — перехват и модификация событий

---

## 🔧 Базовая настройка

```python
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")  # или подставьте напрямую

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Я бот на aiogram.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧩 Маршруты и роутеры

Можно разделять обработчики по файлам:

```python
from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def echo_handler(msg: Message):
    await msg.answer(msg.text)
```

И регистрировать в `Dispatcher`:

```python
dp.include_router(router)
```

---

## 💬 Обработка команд и текстов

```python
from aiogram.filters import Command, Text

@router.message(Command("help"))
async def help_handler(msg: Message):
    await msg.answer("Вот что я умею...")

@router.message(Text(text="Привет"))
async def greet(msg: Message):
    await msg.answer("И тебе привет!")
```

---

## 🔄 FSM — состояние диалогов

```python
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class Form(StatesGroup):
    name = State()
    age = State()

@router.message(Command("fill"))
async def start_form(msg: Message, state: FSMContext):
    await msg.answer("Как тебя зовут?")
    await state.set_state(Form.name)

@router.message(Form.name)
async def process_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@router.message(Form.age)
async def process_age(msg: Message, state: FSMContext):
    data = await state.update_data(age=msg.text)
    await msg.answer(f"Принято: {data['name']}, {data['age']} лет.")
    await state.clear()
```

---

## 🛡️ Middleware (например, логгинг)

```python
from aiogram.dispatcher.middlewares.base import BaseMiddleware

class SimpleLogger(BaseMiddleware):
    async def __call__(self, handler, event, data):
        print(f"Получено сообщение: {event}")
        return await handler(event, data)

dp.message.middleware(SimpleLogger())
```

---

## 📦 Отправка сообщений, фото и пр.

```python
await bot.send_message(chat_id, "Привет!")
await message.answer_photo(photo_url)
await message.reply("Ответ на сообщение")
```

---

## 📎 Работа с кнопками (inline/markup)

```python
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Нажми", callback_data="clicked")]
])

@router.message(Command("menu"))
async def show_menu(msg: Message):
    await msg.answer("Меню:", reply_markup=kb)

@router.callback_query()
async def handle_click(query: types.CallbackQuery):
    await query.answer("Кнопка нажата!")
    await query.message.edit_text("Спасибо за клик!")
```

---

## ✅ Рекомендации

* Используй `.env` и `dotenv` для конфигурации
* Структурируй код: `routers/`, `handlers/`, `middlewares/`, `keyboards/`
* Добавь `logging` или `structlog` для логов
* Используй `async` и `await` строго — не смешивай с sync-кодом

---

## 📚 Полезные ресурсы

* Документация: [https://docs.aiogram.dev/en/latest/](https://docs.aiogram.dev/en/latest/)
* Шаблон проекта: [https://github.com/aiogram/aiogram-template](https://github.com/aiogram/aiogram-template)

---
