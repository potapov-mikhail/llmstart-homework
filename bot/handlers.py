from aiogram import types
from aiogram.filters import Command
import structlog
from config import get_llm_config, get_openrouter_keys, get_system_prompt
from llm.client import create_client, format_messages, generate_response

logger = structlog.get_logger()

# История сообщений в памяти (chat_id -> list)
user_histories = {}

async def register_handlers(dp):
    @dp.message(Command("start"))
    async def start_handler(message: types.Message):
        logger.info("start_command", chat_id=message.chat.id)
        user_histories[message.chat.id] = []
        await message.answer(
            "👋 Привет! Я LLMstart Assistant.\n\n"
            "Я могу отвечать на ваши вопросы с помощью ИИ.\n"
            "Просто напишите сообщение — и получите ответ!\n\n"
            "Доступно:\n"
            "• Диалог с ИИ (до 5 сообщений в истории)\n"
            "• Команда /help — описание возможностей"
        )

    @dp.message(Command("help"))
    async def help_handler(message: types.Message):
        await message.answer(
            "ℹ️ Возможности LLMstart Assistant:\n\n"
            "— Ответы на любые вопросы с помощью LLM\n"
            "— Поддержка диалога (до 5 сообщений в истории)\n"
            "— Быстрый и простой интерфейс\n\n"
            "Просто напишите свой вопрос!"
        )

    @dp.message()
    async def llm_handler(message: types.Message):
        chat_id = message.chat.id
        text = message.text
        if not text:
            return
        # История
        history = user_histories.get(chat_id, [])
        # Формируем сообщения
        system_prompt = get_system_prompt()
        messages = format_messages(history, text, system_prompt)
        # LLM config
        llm_config = get_llm_config()
        keys = get_openrouter_keys()
        client = create_client(keys["api_key"], keys["base_url"])
        try:
            logger.info("llm_request", chat_id=chat_id, prompt=text)
            response = generate_response(client, messages, llm_config)
            await message.answer(response)
            # Обновляем историю (только последние 5)
            history.append({"role": "user", "content": text})
            history.append({"role": "assistant", "content": response})
            user_histories[chat_id] = history[-5:]
        except Exception as e:
            logger.error("llm_error", chat_id=chat_id, error=str(e))
            await message.answer("Извините, не удалось обработать запрос")